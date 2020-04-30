from datetime import datetime

from django.conf import settings

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_notifications.models import HealthcareUnitCapacity
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_notifications" / "data" / "healthcare_unit_capacity" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_STAGING = "staging"

    context_choices = (CONTEXT_STAGING,)

    app = "notifications"
    model = "healthcare_unit_capacity"
    model_verbose_name = "healthcare unit capacity"
    model_verbose_name_plural = "healthcare unit capacities"

    def seed(self):
        if self.context == self.CONTEXT_STAGING:
            self.seed_from_csv(CSV_DIR / "staging")
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def fetch_model(self, row):
        capacity = HealthcareUnitCapacity()
        capacity.notifier = HealthcareUnitNotifier.objects.get(
            user__email=row.get("email"), healthcare_unit__cnes_id=row.get("cnes_id")
        )
        capacity.date = datetime.strptime(row.get("date"), "%Y-%m-%d").date()
        capacity.clinical_adult_beds = int(row.get("cab"))
        capacity.clinical_pediatric_beds = int(row.get("cpb"))
        capacity.icu_adult_beds = int(row.get("iab"))
        capacity.icu_pediatric_beds = int(row.get("ipb"))
        return capacity
