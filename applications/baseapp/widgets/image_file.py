from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext_lazy as _

from PIL import Image

__all__ = ['AdminImageFileWidget']


def is_image(file):
    try:
        with Image.open(file) as image_pointer:
            return image_pointer.size
    except IOError:
        return False


class AdminImageFileWidget(AdminFileWidget):
    """
    Example usage in: `admin.py`

        from baseapp.widgets import AdminImageFileWidget
        from django.db import models

        class MyModelAdmin(admin.ModelAdmin):
            formfield_overrides = {
                models.FileField: {'widget': AdminImageFileWidget},
            }

    """

    def render(self, name, value, attrs=None, renderer=None):
        widget = super().render(name, value, attrs)
        if value:
            possible_image = is_image(value)
            if possible_image:
                widget = (
                    '<div class="admin-image-preview {object_name}">'
                    '<img style="max-height: 200px;" src="{image_url}">'
                    '<p class="file-upload">{dimensions}: {width} x {height}</p>'
                    '</div>'
                    '{widget}'
                    ''.format(
                        object_name='{0}-preview'.format(name),
                        image_url='{0}{1}'.format(settings.MEDIA_URL, value),
                        dimensions=_('Dimensions'),
                        width=possible_image[0],
                        height=possible_image[1],
                        widget=widget,
                    )
                )
        return widget
