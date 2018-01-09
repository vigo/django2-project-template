from django.views.generic.base import TemplateView
from django.utils.text import slugify

from .mixins import HtmlDebugMixin

from baseapp.utils import (
    console,
    numerify,
    urlify,
)

console.configure(
    source='baseapp/views.py',
)

class IndexView(HtmlDebugMixin, TemplateView):
    template_name = 'baseapp/index.html'

    def get_context_data(self, **kwargs):
        self.hdbg('This', 'is', 'an', 'example', 'of')
        self.hdbg('self.hdbg', 'usage')
        self.hdbg(self.request.__dict__)
        self.hdbg(slugify(urlify('Merhaba Dünya! Ben Uğur Özyılmazel')))
        kwargs = super().get_context_data(**kwargs)
        
        query_string_p = numerify(self.request.GET.get('p'))
        console(query_string_p, type(query_string_p),)
        console.dir(self.request.user)
        return kwargs
