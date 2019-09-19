from django.views.generic.base import TemplateView

from ..mixins import HtmlDebugMixin
from ..utils import console, numerify

__all__ = ['IndexView']

console = console(source=__name__)


class IndexView(HtmlDebugMixin, TemplateView):
    template_name = 'baseapp/index.html'

    def get_context_data(self, **kwargs):
        self.hdbg('This', 'is', 'an', 'example', 'of')
        self.hdbg('self.hdbg', 'usage')
        self.hdbg(self.request.META)
        kwargs = super().get_context_data(**kwargs)

        query_string_p = numerify(self.request.GET.get('p'))
        console(query_string_p, type(query_string_p))
        console.dir(self.request.user)
        return kwargs
