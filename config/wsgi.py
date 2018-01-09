import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings.{}'.format(os.environ.get('DJANGO_ENV')))

application = get_wsgi_application()
