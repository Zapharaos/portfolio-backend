import os

from django.conf import settings
from django.core.management.base import BaseCommand

from user.models import File


class Command(BaseCommand):
    help = 'Delete media files under MEDIA_ROOT that no File record references.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='List orphan files without deleting them.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Absolute paths still referenced by a File record.
        referenced = set()
        for record in File.objects.exclude(file='').exclude(file__isnull=True):
            try:
                referenced.add(os.path.normpath(record.file.path))
            except (ValueError, NotImplementedError):
                pass

        media_root = str(settings.MEDIA_ROOT)
        removed = 0
        for root, _dirs, files in os.walk(media_root):
            for name in files:
                path = os.path.normpath(os.path.join(root, name))
                if path in referenced:
                    continue
                self.stdout.write(f'orphan: {os.path.relpath(path, media_root)}')
                if not dry_run:
                    os.remove(path)
                removed += 1

        verb = 'Would remove' if dry_run else 'Removed'
        self.stdout.write(self.style.SUCCESS(f'{verb} {removed} orphan file(s).'))
