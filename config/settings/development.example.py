from .base import *

from baseapp.libs.log_helpers import (
    CustomWerkzeugLogFormatter,
    CustomSqlLogFormatter,
    werkzueg_filter_extenstions_callback,
)

DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'development.sqlite3'),
    }
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CUSTOM_LOGGER_OPTIONS = {
    'hide_these_extensions': ['css', 'js', 'png', 'jpg', 'svg', 'gif', 'woff'],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'werkzueg_filter_extensions': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': werkzueg_filter_extenstions_callback,
        },
    },
    'formatters': {
        'custom_sql_query': {
            '()': CustomSqlLogFormatter,
            'format': '%(levelname)s |\n%(sql)s\n\ntook: %(duration)f mseconds\n\n',
        },
        'custom_werkzeug_log_formatter': {
            '()': CustomWerkzeugLogFormatter,
            'format': '%(levelname)s | %(message)s',
        },
    },
    'handlers': {
        'console_sql': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom_sql_query',
        },
        'console_custom': {
            'level': 'DEBUG',
            'filters': ['werkzueg_filter_extensions'],
            'class': 'logging.StreamHandler',
            'formatter': 'custom_werkzeug_log_formatter',
        }
    },
    'loggers': {
        'werkzeug': {
            'handlers': ['console_custom'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'user_logger': {
            'handlers': ['console_custom'],
            'level': 'DEBUG',
        },
        # enable this block if you want to see SQL queries :)
        # 'django.db.backends': {
        #     'handlers': ['console_sql'],
        #     'level': 'DEBUG',
        # },
    }
}

# middlewares for development purposes only
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# apps for development purposes only
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]
