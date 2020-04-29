from django import forms

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCapacity


class NotifyCapacityForm(forms.ModelForm):
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

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["notifier"].queryset = HealthcareUnitNotifier.objects.filter(
            user=user, is_authorized=True
        )
