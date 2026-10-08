from django import forms
from django.utils.translation import gettext_lazy as _

from core.models import ContactRequest


class ContactRequestForm(forms.ModelForm):
    interest = forms.ChoiceField(
        choices=[("", _("Choose an area of interest")), *ContactRequest.Interest.choices],
        label=_("Area of interest"),
    )
    consent_to_contact = forms.BooleanField(
        required=True,
        label=_("I agree that my details may be used to respond to this enquiry."),
    )

    class Meta:
        model = ContactRequest
        fields = ["name", "email", "company", "phone", "interest", "message", "consent_to_contact"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": _("Your name")}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": _("you@company.com")}),
            "company": forms.TextInput(attrs={"autocomplete": "organization", "placeholder": _("Company name")}),
            "phone": forms.TelInput(attrs={"autocomplete": "tel", "placeholder": _("Optional")}),
            "interest": forms.Select(),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": _("Tell us a little about what you are working on.")}),
        }

    def clean_name(self):
        return " ".join(self.cleaned_data["name"].split())

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 20:
            raise forms.ValidationError(_("Please add a little more detail (at least 20 characters)."))
        return message
