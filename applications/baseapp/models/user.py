from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from baseapp.utils import save_file as custom_save_file


__all__ = [
    'User',
]


class UserManager(BaseUserManager):
    """
    Our custom User model's basic needs.
    """

    use_in_migrations = True

    def create_user(self, email, first_name, last_name, middle_name=None, password=None):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user_create_fields = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

        if middle_name:
            user_create_fields['middle_name'] = middle_name

        user = self.model(**user_create_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, middle_name=None, password=None):
        user = self.create_user(email, first_name, last_name, middle_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def save_user_avatar(instance, filename):
    return custom_save_file(instance, filename, upload_to='avatar/')


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At'),
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('email address'),
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_('first name'),
    )
    middle_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('middle name'),
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_('last name'),
    )
    avatar = models.FileField(
        upload_to=save_user_avatar,
        verbose_name=_('Profile Image'),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('staff status'),
    )

    objects = UserManager()

    class Meta:
        app_label = 'baseapp'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        params = {
            'first_name': self.first_name,
            'middle_name': ' ',
            'last_name': self.last_name,
        }
        if self.middle_name:
            params['middle_name'] = ' {middle_name} '.format(
                middle_name=self.middle_name)
        full_name = '{first_name}{middle_name}{last_name}'.format(**params)
        return full_name.strip()
