from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Donation

class DonationForm(forms.ModelForm):
    """Form for creating a new donation."""
    class Meta:
        model = Donation
        fields = ["amount", "is_anonymous", "donor_name", "donor_email"]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control", 
                "placeholder": _("Số tiền quyên góp (VNĐ)"),
                "min": "10000" # Example minimum donation
            }),
            "is_anonymous": forms.CheckboxInput(attrs={
                "class": "form-check-input",
                "onclick": "toggleAnonymousFields(this)" # JS function to show/hide name/email
            }),
            "donor_name": forms.TextInput(attrs={
                "class": "form-control anonymous-field", 
                "placeholder": _("Tên của bạn (tùy chọn)")
            }),
            "donor_email": forms.EmailInput(attrs={
                "class": "form-control anonymous-field", 
                "placeholder": _("Email của bạn (tùy chọn)")
            }),
        }
        labels = {
            "amount": _("Số tiền"),
            "is_anonymous": _("Quyên góp ẩn danh?"),
            "donor_name": _("Tên người quyên góp"),
            "donor_email": _("Email người quyên góp"),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        
        # Hide anonymous fields by default if user is logged in
        if self.user and self.user.is_authenticated:
            self.fields["donor_name"].widget = forms.HiddenInput()
            self.fields["donor_email"].widget = forms.HiddenInput()
            self.fields["donor_name"].required = False
            self.fields["donor_email"].required = False
        else:
            # For anonymous users, name/email are optional unless is_anonymous is unchecked
            self.fields["donor_name"].required = False
            self.fields["donor_email"].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_anonymous = cleaned_data.get("is_anonymous")
        
        # If user is logged in and not anonymous, clear anonymous fields
        if self.user and self.user.is_authenticated and not is_anonymous:
            cleaned_data["donor_name"] = None
            cleaned_data["donor_email"] = None
        # If user is anonymous and not checked anonymous, require name/email (optional based on project needs)
        # elif not self.user and not is_anonymous:
        #     if not cleaned_data.get("donor_name"):
        #         self.add_error("donor_name", _("Vui lòng nhập tên của bạn."))
        #     if not cleaned_data.get("donor_email"):
        #         self.add_error("donor_email", _("Vui lòng nhập email của bạn."))
                
        return cleaned_data
