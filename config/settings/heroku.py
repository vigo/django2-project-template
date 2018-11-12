import dj_database_url

from .base import *  # noqa: F403

db_from_env = dj_database_url.config(conn_max_age=500)

DEBUG = False
ALLOWED_HOSTS = [
    # heroku domain here! 'XXXXX.herokuapp.com',
]
DATABASES = {'default': db_from_env}

SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https',
)

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

STATICFILES_STORAGE = (
    'whitenoise.django.GzipManifestStaticFilesStorage'
)
STATIC_ROOT = os.path.join(  # noqa: F405
    BASE_DIR, 'staticfiles'  # noqa: F405
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),  # noqa: F405
)
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
