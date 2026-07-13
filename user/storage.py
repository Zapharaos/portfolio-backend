from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """Overwrite a file when a new upload has the same name, instead of Django's
    default behaviour of appending a random suffix.

    This keeps URLs stable (e.g. the resume is always at the same path) and stops
    old, orphaned copies from piling up on disk."""

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name
