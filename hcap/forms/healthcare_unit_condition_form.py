from django import forms
from material import Layout, Fieldset, Row
from django.utils.translation import gettext_lazy as _

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCondition


class HealthcareUnitConditionForm(forms.ModelForm):
    layout = Layout(
        "notifier",
        "date",
        Fieldset(
            _("SARI clinical cases"),
            Row("sari_adult_clinical_cases", "covid_adult_clinical_cases"),
            Row("sari_pediatric_clinical_cases", "covid_pediatric_clinical_cases"),
        ),
        Fieldset(
            _("SARI ICU cases"),
            Row("sari_adult_icu_cases", "covid_adult_icu_cases"),
            Row("sari_pediatric_icu_cases", "covid_pediatric_icu_cases"),
        ),
        Fieldset(
            _("Non-SARI clinical cases"),
            Row("general_adult_clinical_cases", "general_pediatric_clinical_cases"),
        ),
        Fieldset(
            _("Non-SARI ICU cases"), Row("general_adult_icu_cases", "general_pediatric_icu_cases"),
        ),
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["notifier"].disabled = True
        self.fields["date"].disabled = True
