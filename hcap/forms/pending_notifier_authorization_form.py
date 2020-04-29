from django import forms

from hcap_accounts.models import HealthcareUnitNotifier


class PendingNotifierAuthorizationForm(forms.ModelForm):
    class Meta:
        model = HealthcareUnitNotifier
        fields = ("healthcare_unit", "user", "is_authorized")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["healthcare_unit"].disabled = True
        self.fields["user"].disabled = True
