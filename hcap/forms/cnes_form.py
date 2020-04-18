from django import forms
from django.utils.functional import cached_property

from hcap_institutions.models import HealthcareUnit
from django.utils.translation import gettext_lazy as _


class CNESForm(forms.Form):
    cnes = forms.CharField(
        label="Número de CNES",
        max_length=20,
        help_text="Digite o número de CNES da unidade da qual você é o notificador.",
    )

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = self.request.user

    def clean_cnes(self):
        cnes = self.cleaned_data["cnes"]
        if not HealthcareUnit.objects.filter(cnes_id=cnes).exists():
            raise forms.ValidationError(
                _(
                    "The CNES registry provided is not from a valid healthcare unit."
                    + "\nIf you are certain that the CNES registry is valid, please contact the administrator."
                )
            )
        return cnes

    def save(self, user):
        self.unit.register_notifier(user, authorize=False)
