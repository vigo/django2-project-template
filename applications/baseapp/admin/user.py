from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
)
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ..forms import UserChangeForm, UserCreationForm
from ..models import User
from ..widgets import AdminImageFileWidget

__all__ = ['UserAdmin']


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'user_profile_image',
        'email',
        'first_name',
        'last_name',
    )
    list_display_links = ('email',)
    search_fields = (
        'email',
        'first_name',
        'middle_name',
        'last_name',
    )
    ordering = ('email',)
    fieldsets = (
        (
            _('User information'),
            {
                'fields': (
                    'email',
                    'password',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'avatar',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    formfield_overrides = {
        models.FileField: {'widget': AdminImageFileWidget}
    }

    def user_profile_image(self, obj):
        if obj.avatar:
            return format_html(
                '<img style="max-height: 200px;" src="{0}" alt="{1}">',
                obj.avatar.url,
                obj.get_full_name(),
            )
        else:
            return '---'

    user_profile_image.short_description = _(
        'Profile Image'
    )


admin.site.register(User, UserAdmin)
