import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings

from user.models import File


class OverwriteStorageTests(TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self._tmp.name)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        self._tmp.cleanup()

    def _read(self, record):
        record.file.open('rb')
        try:
            return record.file.read()
        finally:
            record.file.close()

    def test_same_name_overwrites_instead_of_suffixing(self):
        first = File.objects.create(name='CV', file=SimpleUploadedFile('cv.pdf', b'v1'))
        second = File.objects.create(name='CV again', file=SimpleUploadedFile('cv.pdf', b'v2'))

        # Same stable path (no random suffix) and the latest content.
        self.assertEqual(second.file.name, 'cv.pdf')
        self.assertEqual(self._read(second), b'v2')
        # Only one file on disk.
        self.assertEqual(os.listdir(self._tmp.name), ['cv.pdf'])
        first.refresh_from_db()

    def test_deleting_record_removes_file_from_disk(self):
        record = File.objects.create(name='Doc', file=SimpleUploadedFile('doc.pdf', b'x'))
        path = record.file.path
        self.assertTrue(os.path.exists(path))

        record.delete()
        self.assertFalse(os.path.exists(path))

    def test_replacing_with_a_different_name_deletes_the_old_file(self):
        record = File.objects.create(name='Doc', file=SimpleUploadedFile('old.pdf', b'x'))
        old_path = record.file.path

        record.file = SimpleUploadedFile('new.pdf', b'y')
        record.save()

        self.assertFalse(os.path.exists(old_path))
        self.assertTrue(os.path.exists(record.file.path))


class FileAdminFormTests(TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self._tmp.name)
        self.override.enable()
        File.objects.create(name='Existing CV', file=SimpleUploadedFile('cv.pdf', b'v1'))

    def tearDown(self):
        self.override.disable()
        self._tmp.cleanup()

    def _form(self, instance=None):
        from user.admin import FileAdminForm
        return FileAdminForm(
            data={'name': 'New'},
            files={'file': SimpleUploadedFile('cv.pdf', b'v2')},
            instance=instance,
        )

    def test_rejects_a_name_used_by_another_record(self):
        form = self._form()
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
        self.assertIn('already used', form.errors['file'][0])

    def test_allows_replacing_the_same_record_with_the_same_name(self):
        existing = File.objects.get(name='Existing CV')
        form = self._form(instance=existing)
        self.assertTrue(form.is_valid(), form.errors)


class CleanOrphanMediaCommandTests(TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.override = override_settings(MEDIA_ROOT=self._tmp.name)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        self._tmp.cleanup()

    def test_removes_unreferenced_files_only(self):
        referenced = File.objects.create(name='Keep', file=SimpleUploadedFile('keep.pdf', b'k'))
        orphan_path = os.path.join(self._tmp.name, 'orphan.pdf')
        with open(orphan_path, 'wb') as handle:
            handle.write(b'orphan')

        call_command('clean_orphan_media')

        self.assertFalse(os.path.exists(orphan_path))
        self.assertTrue(os.path.exists(referenced.file.path))

    def test_dry_run_keeps_everything(self):
        orphan_path = os.path.join(self._tmp.name, 'orphan.pdf')
        with open(orphan_path, 'wb') as handle:
            handle.write(b'orphan')

        call_command('clean_orphan_media', '--dry-run')

        self.assertTrue(os.path.exists(orphan_path))
