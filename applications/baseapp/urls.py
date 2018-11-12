from django.urls import path

from .views import IndexView

app_name = 'baseapp'

# fmt: off
urlpatterns = [
    path('', view=IndexView.as_view(), name='index')
]
# fmt: on
