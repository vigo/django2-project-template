from django.test import TestCase

from ..models import User


__all__ = [
    'CustomUserTestCase',
]


class CustomUserTestCase(TestCase):

    def test_create_user(self):
        user = User.objects.create(email='foo@bar.com',
                                   first_name='Uğur',
                                   last_name='Özyılmazel',
                                   password='1234',)
        self.assertEqual(user.pk, user.id)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_staffuser(self):
        user = User.objects.create(email='foo@bar.com',
                                   first_name='Uğur',
                                   last_name='Özyılmazel',
                                   password='1234',)
        user.is_staff = True
        user.save()
        self.assertEqual(user.pk, user.id)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        user = User.objects.create(email='foo@bar.com',
                                   first_name='Uğur',
                                   last_name='Özyılmazel',
                                   password='1234',)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.assertEqual(user.pk, user.id)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
