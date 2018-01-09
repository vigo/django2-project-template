import os
import datetime

from django.utils.text import slugify
from baseapp.utils import urlify


__all__ = [
    'save_file',
]


def save_file(instance, filename, upload_to='upload/%Y/%m/%d/'):
    """

    By default, this saves to : `MEDIA_ROOT/upload/2017/09/06/`

    You can customize this. In your `models.py`:

        from baseapp.utils import save_file as custom_save_file

        def my_custom_uploader(instance, filename):

            # do your stuff
            # at the end, call:

            my_custom_upload_path = 'images/%Y/'
            return custom_save_file(instance, filename, upload_to=my_custom_upload_path)

        class MyModel(models.Model):
            image = models.FileField(
                upload_to='my_custom_uploader',
                verbose_name=_('Profile Image'),
            )

    """

    file_basename, file_extension = os.path.splitext(filename)
    file_savename = '{safe_basename}{extension}'.format(
        safe_basename=slugify(urlify(file_basename)),
        extension=file_extension.lower(),
    )
    now = datetime.datetime.now()
    return '{upload_to}{file_savename}'.format(
        upload_to=now.strftime(upload_to),
        file_savename=file_savename,
    )
