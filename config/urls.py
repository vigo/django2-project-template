# pylint: disable=C0103,E0401

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _

from baseapp.views import (
    custom_400_error,
    custom_403_error,
    custom_404_error,
    custom_500_error,
)

admin.site.index_title = _('your admin index title')
admin.site.site_title = _('your site title')
admin.site.site_header = _('your site header')

urlpatterns = [path('admin/', admin.site.urls), path('__baseapp__/', include('baseapp.urls', namespace='baseapp'))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))] + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # for local development only...
    urlpatterns += [
        path('400/', custom_400_error),
        path('403/', custom_403_error),
        path('404/', custom_404_error),
        path('500/', custom_500_error),
    ]


# add your newly created app's urls here!
# urlpatterns += [
# ]

handler400 = custom_400_error
handler403 = custom_403_error
handler404 = custom_404_error
handler500 = custom_500_error
