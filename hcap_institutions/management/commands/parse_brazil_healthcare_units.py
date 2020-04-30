"""
CHANGEME to parse the original csv file
"""

import csv
import json

from django.conf import settings

from hcap_geo.models import Region
from hcap_utils.contrib.management import BaseCommand

HEADER = ("city_id", "cnes_id", "name")
CSV_DIR = settings.BASE_DIR / "hcap_institutions" / "data" / "healthcare_unit" / "csv"
SRC_DIR = settings.BASE_DIR / "hcap_institutions" / "data" / "healthcare_unit" / "src"


class Command(BaseCommand):
    help = "Parse Brazilian healthcare unit data from original csv file"

    def safe_handle(self, *args, **kwargs):
        with open(str(SRC_DIR) + "/healthcare_units.json") as json_file:
            with open(str(CSV_DIR) + "/brazil.csv", "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(HEADER)
                for k, v in json.load(json_file).items():
                    city_id = self.parse_city(v["city_id"])
                    cnes_id = v["cnes_id"]
                    name = v["name"]
                    writer.writerow((city_id, cnes_id, name))

    def parse_city(self, city_id):
        id_length = len(city_id)
        if id_length == 6:
            cities = list(Region.objects.filter(code__startswith=city_id))
            length = len(cities)
            if length == 1:
                return cities[0].code
            elif length == 0:
                self.raise_message(f"City with id {city} not found")
            else:
                self.raise_message(f"There are two or more cities matching {city}")
        elif id_length == 7:
            return city_id
        else:
            self.raise_message(f"ID {city} is not valid")
