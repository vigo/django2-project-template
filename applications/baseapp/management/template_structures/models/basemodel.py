TEMPLATE_MODEL_BASEMODEL = """from django.utils.translation import ugettext_lazy as _
from django.db import models

from baseapp.models import BaseModel


__all__ = [
    '{model_name}',
]


class {model_name}(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )

    class Meta:
        app_label = '{app_name}'
        verbose_name = _('{model_name}')
        verbose_name_plural = _('{model_name}')
    
    def __str__(self):
        return self.title

"""


__all__ = [
    'TEMPLATE_MODEL_BASEMODEL',
]
