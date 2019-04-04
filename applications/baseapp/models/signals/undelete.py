# pylint: disable=C0103

import django.dispatch

__all__ = ['pre_undelete', 'post_undelete']

pre_undelete = django.dispatch.Signal(providing_args=['instance'])
post_undelete = django.dispatch.Signal(providing_args=['instance'])
