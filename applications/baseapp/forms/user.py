from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
)
from django.utils.translation import ugettext_lazy as _

__all__ = ['UserChangeForm', 'UserCreationForm']

User = get_user_model()


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
        label=_('Password'), widget=forms.PasswordInput
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
        if (
            password1
            and password2
            and password1 != password2
        ):
            raise forms.ValidationError(
                _('Passwords don\'t match')
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(
            commit=False
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
