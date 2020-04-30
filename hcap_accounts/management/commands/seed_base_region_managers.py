from django.conf import settings
from django.contrib.auth import get_user_model

from hcap_accounts.models import RegionManager
from hcap_geo.models import Region
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_accounts" / "data" / "region_manager" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_STAGING = "staging"

    context_choices = (CONTEXT_STAGING,)

    app = "accounts"
    model = "region_manager"
    model_verbose_name = "region manager"

    def seed(self):
        if self.context == self.CONTEXT_STAGING:
            self.seed_from_csv(CSV_DIR / "staging")
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def fetch_model(self, row):
        manager = RegionManager()
        manager.user = get_user_model().objects.get(email=row.get("email"))
        manager.region = Region.objects.get(code=row.get("code"))
        manager.is_authorized = bool(row.get("is_authorized"))
        return manager
