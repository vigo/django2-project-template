"""
View template for app generator
"""

TEMPLATE_VIEWS = """import logging

from django.views.generic.base import TemplateView

from baseapp.mixins import HtmlDebugMixin
from baseapp.utils import console

__all__ = ['{app_name_title}View']

logger = logging.getLogger('app')
console = console(source=__name__)


class {app_name_title}View(HtmlDebugMixin, TemplateView):
    template_name = '{app_name}/index.html'

    def get_context_data(self, **kwargs):
        self.hdbg('Hello from hdbg')
        kwargs = super().get_context_data(**kwargs)
        console.dir(self.request.user)
        return kwargs

"""


__all__ = ['TEMPLATE_VIEWS']
