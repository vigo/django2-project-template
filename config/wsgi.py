import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings.{0}'.format(os.environ.setdefault('DJANGO_ENV', 'production'))
)

application = get_wsgi_application()
