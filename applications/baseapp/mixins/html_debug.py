# pylint: disable=W0613

from django.conf import settings
from django.utils import translation

___all___ = ['HtmlDebugMixin']


class HtmlDebugMixin:
    def __init__(self, *args, **kwargs):
        self.debug_output = list()

    def hdbg(self, *args):
        """
        Works only if DEBUG is True
        """

        if settings.DEBUG and args not in self.debug_output:
            self.debug_output.append(args)

    def get_context_data(self, **kwargs):
        """
        Works only if DEBUG is True
        """

        kwargs = super().get_context_data(**kwargs)

        custom_template_variables = {'IS_DEBUG': settings.DEBUG, 'LANG': translation.get_language()}
        kwargs.update(**custom_template_variables)

        if settings.DEBUG:
            kwargs.update(hdbg_data=self.debug_output)
        return kwargs
