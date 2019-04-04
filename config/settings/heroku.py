# pylint: disable=W0401,W0614,C0103

import logging

import dj_database_url

from .base import *  # noqa: F403

db_from_env = dj_database_url.config(conn_max_age=500)

DEBUG = False
ALLOWED_HOSTS = [
    # heroku domain here! 'XXXXX.herokuapp.com',
]
DATABASES = {'default': db_from_env}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # noqa: F405  # noqa: F405

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)  # noqa: F405
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # noqa: F405

# fmt: off
INSTALLED_APPS.insert(  # noqa: F405
    INSTALLED_APPS.index('django.contrib.staticfiles'),  # noqa: F405
    'whitenoise.runserver_nostatic',
)

MIDDLEWARE.insert(  # noqa: F405
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,  # noqa: F405
    'whitenoise.middleware.WhiteNoiseMiddleware',
)
# fmt: on

LOGGING_CONFIG = None
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()  # noqa: F405

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {'default': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}},
        'handlers': {
            'mail_admins': {'level': 'ERROR', 'class': 'django.utils.log.AdminEmailHandler'},
            'stdout': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': sys.stdout,  # noqa: F405
            },
            'stderr': {
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': sys.stderr,  # noqa: F405
            },
        },
        'loggers': {
            '': {'level': 'DEBUG', 'handlers': ['stdout']},
            'app': {'level': LOGLEVEL, 'handlers': ['stdout'], 'propagate': False},
            'django.request': {'handlers': ['mail_admins'], 'level': 'ERROR', 'propagate': False},
        },
    }
)
