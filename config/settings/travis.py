# pylint: disable=W0401,W0614

import dj_database_url

from .base import *  # noqa pylint: disable=E0401

SECRET_KEY = 'fake-key'

DATABASES = {'default': dj_database_url.config(default='postgres://localhost:5432/test_db')}

PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# fix here! this is only for testing BaseModel, BaseModelWithSoftDelete
MIGRATION_MODULES = {'baseapp': None, 'auth': None, 'contenttypes': None}
