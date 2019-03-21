from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BaseappConfig(AppConfig):
    name = 'baseapp'
    verbose_name = _('baseapp')
    verbose_name_plural = _('baseapp')
