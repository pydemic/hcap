from django import forms

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCondition


class NotifyConditionForm(forms.ModelForm):
    class Meta:
        model = HealthcareUnitCondition
        fields = (
            "notifier",
            "date",
            "sari_adult_clinical_cases",
            "covid_adult_clinical_cases",
            "sari_pediatric_clinical_cases",
            "covid_pediatric_clinical_cases",
            "sari_adult_icu_cases",
            "covid_adult_icu_cases",
            "sari_pediatric_icu_cases",
            "covid_pediatric_icu_cases",
            "general_adult_clinical_cases",
            "general_pediatric_clinical_cases",
            "general_adult_icu_cases",
            "general_pediatric_icu_cases",
        )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["notifier"].queryset = HealthcareUnitNotifier.objects.filter(
            user=user, is_authorized=True
        )
