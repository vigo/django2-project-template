# pylint: disable=W0401

import dj_database_url

from .base import *  # noqa pylint: disable=E0401

SECRET_KEY = 'fake-key'

# if you use DATABASE_URL_TEST env-var:
# DATABASES = {'default': dj_database_url.config(env='DATABASE_URL_TEST')}

# or hard-coded :)
DATABASES = {'default': dj_database_url.config(default='postgres://localhost:5432/django2_pt_test')}

PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
