"""
App Config template for app generator
"""

TEMPLATE_APPS = """from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class {app_name_title}Config(AppConfig):
    name = '{app_name}'
    verbose_name = _('{app_name_title}')
    verbose_name_plural = _('{app_name_title}')

"""


__all__ = ['TEMPLATE_APPS']
