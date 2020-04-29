from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_institutions.models import HealthcareUnit


class NotifierAuthorizationRequestForm(forms.Form):
    cnes_id = forms.CharField(
        label=_("CNES registry"),
        max_length=15,
        help_text=_("Write the CNES registry of the healthcare unit you are notifier."),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    @cached_property
    def healthcare_unit(self):
        cnes_id = self.cleaned_data["cnes_id"]
        return HealthcareUnit.objects.get(cnes_id=cnes_id)

    def clean_cnes_id(self):
        cnes_id = self.cleaned_data["cnes_id"]

        if not HealthcareUnit.objects.filter(cnes_id=cnes_id).exists():
            raise forms.ValidationError(
                _(
                    "The CNES registry provided is not from a valid healthcare unit."
                    + "\nIf you are certain that the CNES registry is valid, please contact the administrator."
                )
            )

        return cnes_id

    def save(self):
        notifier = HealthcareUnitNotifier(
            user=self.user, healthcare_unit=self.healthcare_unit, is_authorized=False
        )
        notifier.full_clean()
        notifier.save()
