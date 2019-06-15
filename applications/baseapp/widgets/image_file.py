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
            possible_image = is_image(value.path)
            if possible_image:
                object_name = f'{name}-preview'
                widget = (
                    f'<div class="admin-image-preview {object_name}">'
                    f'<img class="thumbnail" src="{value.url}">'
                    f'<p class="file-upload">{_("Dimensions")}: {possible_image[0]} x {possible_image[1]}</p>'
                    f'</div>{widget}'
                )
        return widget
