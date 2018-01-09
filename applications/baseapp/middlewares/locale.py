from django.utils.cache import patch_vary_headers
from django.utils import translation


__all__ = [
    'CustomLocaleMiddleware',
]


class CustomLocaleMiddleware(object):
    """
    `/en/path/to/page/` sets `request.LANGUAGE_CODE` to `en` otherwise `tr`.

    add this manually to your `MIDDLEWARE` list:

    # settings/base.py

    MIDDLEWARE += [
        'baseapp.middlewares.CustomLocaleMiddleware',
    ]

    You can access it via `request.LANGUAGE_CODE`

    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META['PATH_INFO'].startswith('/en'):
            language = 'en'
        else:
            language = 'tr'

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        response = self.get_response(request)

        patch_vary_headers(response, ('Accept-Language',))
        response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
