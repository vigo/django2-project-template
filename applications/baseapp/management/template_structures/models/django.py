"""
Django Model template for model generator
"""

TEMPLATE_MODEL_DJANGO = """import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from baseapp.utils import console

__all__ = ['{model_name_title}']

logger = logging.getLogger('app')
console = console(source=__name__)


class {model_name_title}(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    title = models.CharField(max_length=255, verbose_name=_('title'))

    class Meta:
        app_label = '{app_name}'
        verbose_name = _('{model_name}')
        verbose_name_plural = _('{model_name}s')  # check pluralization

    def __str__(self):
        return self.title

"""


__all__ = ['TEMPLATE_MODEL_DJANGO']
