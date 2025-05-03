from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile information."""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('First Name')})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Last Name')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Email'), 'readonly': True})
