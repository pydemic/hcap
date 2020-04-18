from django.conf import settings

from hcap_geo.models import Region
from hcap_institutions.models import HealthcareUnit
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_institutions" / "data" / "healthcare_unit" / "csv"


class Command(BaseSeedCommand):
    app = "institutions"
    model = "healthcare_unit"
    model_verbose_name = "healthcare unit"

    def seed(self):
        self.seed_from_csv(CSV_DIR / "brazil")

    def fetch_model(self, row):
        healthcare_unit = HealthcareUnit()
        healthcare_unit.city = self.get_city(row["city_id"])
        healthcare_unit.cnes_id = row.get("cnes_id")
        healthcare_unit.name = row.get("name")
        return healthcare_unit

    def get_city(self, city_id):
        try:
            return Region.objects.get(code=city_id)
        except Exception:
            self.raise_message(f"City with code {city_id} not found")
