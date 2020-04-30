from django.conf import settings
from django.contrib.auth import get_user_model

from hcap_accounts.models import HealthcareUnitNotifier
from hcap_institutions.models import HealthcareUnit
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_accounts" / "data" / "healthcare_unit_notifier" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_STAGING = "staging"

    context_choices = (CONTEXT_STAGING,)

    app = "accounts"
    model = "healthcare_unit_notifier"
    model_verbose_name = "healthcare unit notifier"

    def seed(self):
        if self.context == self.CONTEXT_STAGING:
            self.seed_from_csv(CSV_DIR / "staging")
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def fetch_model(self, row):
        notifier = HealthcareUnitNotifier()
        notifier.user = get_user_model().objects.get(email=row.get("email"))
        notifier.healthcare_unit = HealthcareUnit.objects.get(cnes_id=row.get("cnes_id"))
        notifier.is_authorized = bool(row.get("is_authorized"))
        return notifier
