# pylint: disable=W0401

import dj_database_url

from .base import *  # noqa pylint: disable=E0401

DATABASES = {'default': dj_database_url.config()}

PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
