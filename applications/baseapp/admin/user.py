from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
)
from django.contrib.auth.models import Permission
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from ..forms import UserChangeForm, UserCreationForm
from ..models import User
from ..utils import console
from ..widgets import AdminImageFileWidget

__all__ = ['UserAdmin']

console = console(source=__name__)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    autocomplete_fields = ['groups', 'user_permissions']
    list_display = ('user_profile_image', 'email', 'first_name', 'last_name')
    list_display_links = ('email',)
    search_fields = ('email', 'first_name', 'middle_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (_('user information'), {'fields': ('email', 'password', 'first_name', 'middle_name', 'last_name', 'avatar')}),
        (_('permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}),
    )
    formfield_overrides = {
        models.FileField: {'widget': AdminImageFileWidget},
        models.CharField: {'widget': TextInput(attrs={'size': 100})},
    }

    # pylint: disable=R0201
    def user_profile_image(self, obj):
        if obj.avatar:
            return format_html('<img class="thumbnail" src="{0}" alt="{1}">', obj.avatar.url, obj.get_full_name())
        return '---'

    user_profile_image.short_description = _('profile image')

    class Media:
        css = {'all': ['admin/baseapp.css']}
