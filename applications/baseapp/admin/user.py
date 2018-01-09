from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from ..models import User
from baseapp.widgets import AdminImageFileWidget


__all__ = [
    'UserAdmin',
]


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        label=_('Password'),
        help_text=_(
            'Raw passwords are not stored, so there is no way to see this '
            'user\'s password, but you can change the password using '
            '<a href="../password/">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        labels = {
            'first_name': _('first name').title(),
            'last_name': _('last name').title(),
        }

    def clean_password(self):
        return self.initial['password']


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
    )

    class Meta:
        """
        `fields` property holds only required fields.
        """

        model = User
        fields = ('first_name', 'last_name')
        labels = {
            'first_name': _('first name').title(),
            'last_name': _('last name').title(),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords don\'t match'))
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('user_profile_image', 'email', 'first_name', 'last_name')
    list_display_links = ('email',)
    search_fields = ('email', 'first_name', 'middle_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (_('User information'), {'fields': (
            'email',
            'password',
            'first_name',
            'middle_name',
            'last_name',
            'avatar',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        }),
    )
    formfield_overrides = {
        models.FileField: {'widget': AdminImageFileWidget},
    }

    def user_profile_image(self, obj):
        if obj.avatar:
            return format_html('<img style="max-height: 200px;" src="{}" alt="{}">',
                               obj.avatar.url,
                               obj.get_full_name(),
                               )
        else:
            return '---'
    user_profile_image.short_description = _('Profile Image')


admin.site.register(User, UserAdmin)
