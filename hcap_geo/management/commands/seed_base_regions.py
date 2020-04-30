from django.conf import settings

from hcap_geo.models import Region
from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_geo" / "data" / "region" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_BRAZIL = "brazil"

    app = "geo"
    model = "region"

    context_choices = (CONTEXT_BRAZIL,)

    def seed(self):
        if self.context == self.CONTEXT_BRAZIL:
            self.seed_brazil_data()
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def seed_brazil_data(self):
        self.seed_from_csv(CSV_DIR / "1_world")
        self.seed_from_csv(CSV_DIR / "2_continents")
        self.seed_from_csv(CSV_DIR / "3_countries")

        brazil_dir = CSV_DIR / "3_countries/076_brazil"

        self.seed_from_csv(brazil_dir / "4_regioes")
        self.seed_from_csv(brazil_dir / "4_regioes_lat_lng")
        self.seed_from_csv(brazil_dir / "5_ufs")
        self.seed_from_csv(brazil_dir / "5_ufs_lat_lng")
        self.seed_from_csv(brazil_dir / "6_mesorregioes")
        self.seed_from_csv(brazil_dir / "6_microrregioes")
        self.seed_from_csv(brazil_dir / "7_municipios")

    def fetch_model(self, row):
        kind = int(row["kind"])
        parent_hierarchy = row["parent_hierarchy"]
        code = row["code"]

        try:
            region = Region.objects.get(kind=kind, parent_hierarchy=parent_hierarchy, code=code)
        except Exception:
            region = Region(kind=kind, parent_hierarchy=parent_hierarchy, code=code)

        name = row.get("name")
        if name not in [None, ""]:
            region.name = name

        abbr = row.get("abbr")
        if abbr not in [None, ""]:
            region.abbr = abbr

        lat = row.get("lat")
        lng = row.get("lng")
        if lat not in [None, ""] and lng not in [None, ""]:
            region.lat = lat
            region.lng = lng

        return region

    def fetch_relations(self, region, row):
        queries = row.get("parents")

        if queries not in [None, ""]:
            parents = []

            for query in queries.split(";"):
                queryset = Region.objects

                for query_item in query.split("&"):
                    (kind, code) = query_item.split("=")
                    kind = int(kind)

                    if isinstance(queryset, Region):
                        queryset = queryset.children.get(kind=kind, code=code)
                    else:
                        queryset = queryset.get(kind=kind, code=code)

                if isinstance(queryset, Region):
                    parents.append(queryset)
                else:
                    self.raise_message(f'Parent "{query}" not found')

            if len(parents) > 0:
                region.parents.set(parents)
