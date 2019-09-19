import os

from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from .utils import console

__all__ = ['FileNotFoundFileSystemStorage', 'OverwriteStorage']

console = console(source=__name__)

FILE_NOT_FOUND_IMAGE = 'images/file-not-found.jpg'


class FileNotFoundFileSystemStorage(FileSystemStorage):
    @property
    def file_not_found_image_path(self):
        app_config = apps.get_app_config('baseapp')
        return os.path.join(app_config.path, 'static', FILE_NOT_FOUND_IMAGE)

    def _open(self, name, mode='rb'):
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return super()._open(name, mode)
        return File(open(self.file_not_found_image_path, mode))

    def size(self, name):
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return super().size(name)
        return 0

    def url(self, name):
        url = super().url(name)
        if self.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return url
        return f'{settings.STATIC_URL}{FILE_NOT_FOUND_IMAGE}'


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
