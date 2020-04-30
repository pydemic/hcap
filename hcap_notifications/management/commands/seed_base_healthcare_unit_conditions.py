from datetime import datetime

from django.conf import settings

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCondition
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_notifications" / "data" / "healthcare_unit_condition" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_STAGING = "staging"

    context_choices = (CONTEXT_STAGING,)

    app = "notifications"
    model = "healthcare_unit_condition"
    model_verbose_name = "healthcare unit condition"

    def seed(self):
        if self.context == self.CONTEXT_STAGING:
            self.seed_from_csv(CSV_DIR / "staging")
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def fetch_model(self, row):
        condition = HealthcareUnitCondition()
        condition.notifier = HealthcareUnitNotifier.objects.get(
            user__email=row.get("email"), healthcare_unit__cnes_id=row.get("cnes_id")
        )
        condition.date = datetime.strptime(row.get("date"), "%Y-%m-%d").date()
        condition.sari_adult_clinical_cases = int(row.get("sacc"))
        condition.covid_adult_clinical_cases = int(row.get("cacc"))
        condition.sari_pediatric_clinical_cases = int(row.get("spcc"))
        condition.covid_pediatric_clinical_cases = int(row.get("cpcc"))
        condition.sari_adult_icu_cases = int(row.get("saic"))
        condition.covid_adult_icu_cases = int(row.get("caic"))
        condition.sari_pediatric_icu_cases = int(row.get("spic"))
        condition.covid_pediatric_icu_cases = int(row.get("cpic"))
        condition.general_adult_clinical_cases = int(row.get("gacc"))
        condition.general_pediatric_clinical_cases = int(row.get("gpcc"))
        condition.general_adult_icu_cases = int(row.get("gaic"))
        condition.general_pediatric_icu_cases = int(row.get("gpic"))
        return condition
