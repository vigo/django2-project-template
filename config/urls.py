from django.conf import settings
from django.urls import (
    path,
    include,
)
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__baseapp__/', include('baseapp.urls', namespace='baseapp')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add your newly created app's urls here!
# urlpatterns += [
#
# ]