TEMPLATE_URLS = """from django.urls import path

from .views import {app_name_title}View

app_name = '{app_name}'
urlpatterns = [
    path('', view={app_name_title}View.as_view(), name='{app_name}_index'),
]

"""


__all__ = ['TEMPLATE_URLS']
