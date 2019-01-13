import logging.config

import dj_database_url

from .base import *  # isort:skip # noqa: F403


DEBUG = False

ALLOWED_HOSTS = ['.your.domain.com']

# Set your DATABASE_URL environment variable.
# Example:
# DATABASE_URL=postgres://USER:PASS@DATABASE:5432/TABLE
DATABASES = {'default': dj_database_url.config()}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# Production only apps
# INSTALLED_APPS += [
#     'raven.contrib.django.raven_compat',
# ]

# Ubuntu ...
FILE_UPLOAD_PERMISSIONS = 0o644

PRODUCTION_BASE_PATH = (
    '/home/deployer/your.domain.com/files/'
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(  # noqa: F405
    PRODUCTION_BASE_PATH, 'static_root/'
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(  # noqa: F405
    PRODUCTION_BASE_PATH, 'media_root/'
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),  # noqa: F405
)

LOGGING_CONFIG = None
LOGLEVEL = os.environ.get(  # noqa: F405
    'LOGLEVEL', 'info'
).upper()

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            },
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
            'app': {
                'level': LOGLEVEL,
                'handlers': ['stdout'],
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }
)

ADMINS = (('Your Name', 'your@email.com'),)
MANAGERS = ADMINS

# Error reporting via email
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = 'os.environ.get('DEFAULT_FROM_EMAIL')
# EMAIL_SUBJECT_PREFIX = '[MY-SITE-NAME] '
