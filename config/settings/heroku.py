# pylint: disable=W0401,W0614,C0103

import logging.config

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
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
DJANGO_LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'INFO')  # noqa: F405

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
            'slack': {'level': 'ERROR', 'class': 'baseapp.utils.log.SlackExceptionHandler'},
        },
        'loggers': {
            '': {'level': 'DEBUG', 'handlers': ['stdout']},
            'app': {'level': DJANGO_LOG_LEVEL, 'handlers': ['stdout'], 'propagate': False},
            'django.request': {'handlers': ['mail_admins', 'slack'], 'level': 'ERROR', 'propagate': False},
        },
    }
)

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_HOST = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_NAME = ''

X_FRAME_OPTIONS = 'DENY'

# ADMINS = (('Your Name', 'your@email.com'),)
# MANAGERS = ADMINS

# Error reporting via email
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = 'os.environ.get('DEFAULT_FROM_EMAIL')
# EMAIL_SUBJECT_PREFIX = '[MY-SITE-NAME] '
