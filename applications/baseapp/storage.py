import os

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

__all__ = ['FileNotFoundFileSystemStorage']

FILE_NOT_FOUND_IMAGE = 'file-not-found.jpg'


class FileNotFoundFileSystemStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return super()._open(name, mode)
        dummy_file = os.path.join(settings.STATICFILES_DIRS[0], FILE_NOT_FOUND_IMAGE)
        return File(open(dummy_file, mode))

    def size(self, name):
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return super().size(name)
        return 0

    def url(self, name):
        url = super().url(name)
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return url
        return f'{settings.STATIC_URL}{FILE_NOT_FOUND_IMAGE}'
