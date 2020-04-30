from django import forms
from material import Layout, Fieldset, Row
from django.utils.translation import gettext_lazy as _
from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCapacity


class HealthcareUnitCapacityForm(forms.ModelForm):
    layout = Layout(
        "notifier",
        "date",
        Fieldset(_("Clinical beds"), Row("clinical_adult_beds", "clinical_pediatric_beds")),
        Fieldset(_("ICU beds"), Row("icu_adult_beds", "icu_pediatric_beds")),
    )

    class Meta:
        model = HealthcareUnitCapacity
        fields = (
            "notifier",
            "date",
            "clinical_adult_beds",
            "clinical_pediatric_beds",
            "icu_adult_beds",
            "icu_pediatric_beds",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["notifier"].disabled = True
        self.fields["date"].disabled = True
