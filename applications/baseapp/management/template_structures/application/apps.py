TEMPLATE_APPS = """from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class {app_name_title}Config(AppConfig):
    name = '{app_name}'
    verbose_name = _('{app_name_title}')
    verbose_name_plural = _('{app_name_title}')

"""


__all__ = [
    'TEMPLATE_APPS',
]