from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, label=_("First Name"), required=True
    )
    last_name = forms.CharField(
        max_length=30, label=_("Last Name"), required=True
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
