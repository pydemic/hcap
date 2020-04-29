import csv

import requests
from django.conf import settings

from hcap_utils.contrib.management import BaseCommand
from hcap_geo.models import Region

BASE_URL = "https://servicodados.ibge.gov.br/api/v1/"
CSV_DIR = settings.BASE_DIR / "hcap_geo" / "data" / "region" / "csv" / "3_countries" / "076_brazil"
HEADER = ("kind", "parent_hierarchy", "parents", "code", "name", "abbr", "lat", "lng")
SOUTH_AMERICA_CODE = "6"
BRAZIL_CODE = "76"
KIND_COUNTRY = str(Region.KIND_COUNTRY)
KIND_MACROREGION = str(Region.KIND_MACROREGION)
KIND_STATE = str(Region.KIND_STATE)
KIND_MESOREGION = str(Region.KIND_MESOREGION)
KIND_CITY = str(Region.KIND_CITY)


class Command(BaseCommand):
    help = "Fetch Brazilian geographic data from IBGE official API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="If set, fetch all data from IBGE",
        )

        parser.add_argument(
            "--regiao",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='If set, fetch macroregions named "região" from IBGE',
        )

        parser.add_argument(
            "--uf",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='If set, fetch states named "uf" from IBGE',
        )

        parser.add_argument(
            "--mesorregiao",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='If set, fetch mesoregions named "mesorregiao" from IBGE',
        )

        parser.add_argument(
            "--microrregiao",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='If set, fetch mesoregions named "microrregiao" from IBGE',
        )

        parser.add_argument(
            "--municipio",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help='If set, fetch cities named "municipio" from IBGE',
        )

    def safe_handle(
        self,
        all=False,
        regiao=False,
        uf=False,
        mesorregiao=False,
        microrregiao=False,
        municipio=False,
        **options,
    ):
        if all:
            regiao = uf = mesorregiao = microrregiao = municipio = True

        if regiao:
            self.fetch_regiao()
        if uf:
            self.fetch_uf()
        if mesorregiao:
            self.fetch_mesorregiao()
        if microrregiao:
            self.fetch_microrregiao()
        if municipio:
            self.fetch_municipio()

    def fetch_regiao(self):
        def row(region):
            return (
                KIND_MACROREGION,
                to_hierarchy(SOUTH_AMERICA_CODE, BRAZIL_CODE),
                to_query({KIND_COUNTRY: BRAZIL_CODE}),
                region["id"],
                region["nome"],
                region["sigla"],
                None,
                None,
            )

        fetch("localidades/regioes", "4_regioes.csv", row)

    def fetch_uf(self):
        def row(state):
            region_id = str(state["regiao"]["id"])
            return (
                KIND_STATE,
                to_hierarchy(SOUTH_AMERICA_CODE, BRAZIL_CODE),
                to_query(
                    {KIND_COUNTRY: BRAZIL_CODE},
                    {KIND_COUNTRY: BRAZIL_CODE, KIND_MACROREGION: region_id},
                ),
                state["id"],
                state["nome"],
                state["sigla"],
                None,
                None,
            )

        fetch("localidades/estados", "5_ufs.csv", row)

    def fetch_mesorregiao(self):
        def row(mesoregion):
            state_id = str(mesoregion["UF"]["id"])
            name = mesoregion["nome"]
            return (
                KIND_MESOREGION,
                to_hierarchy(SOUTH_AMERICA_CODE, BRAZIL_CODE, state_id),
                to_query({KIND_COUNTRY: BRAZIL_CODE, KIND_STATE: state_id}),
                mesoregion["id"],
                name,
                name,
                None,
                None,
            )

        fetch("localidades/mesorregioes", "6_mesorregioes.csv", row)

    def fetch_microrregiao(self):
        def row(microregion):
            mesoregion = microregion["mesorregiao"]
            mesoregion_id = str(mesoregion["id"])
            state_id = str(mesoregion["UF"]["id"])
            name = microregion["nome"]
            return (
                KIND_MESOREGION,
                to_hierarchy(SOUTH_AMERICA_CODE, BRAZIL_CODE, state_id),
                to_query(
                    {KIND_COUNTRY: BRAZIL_CODE, KIND_STATE: state_id},
                    {
                        KIND_COUNTRY: BRAZIL_CODE,
                        KIND_STATE: state_id,
                        KIND_MESOREGION: mesoregion_id,
                    },
                ),
                microregion["id"],
                name,
                name,
                None,
                None,
            )

        fetch("localidades/microrregioes", "6_microrregioes.csv", row)

    def fetch_municipio(self):
        def row(municipality):
            microregion = municipality["microrregiao"]
            microregion_id = str(microregion["id"])
            mesoregion = microregion["mesorregiao"]
            mesoregion_id = str(mesoregion["id"])
            state_id = str(mesoregion["UF"]["id"])
            name = municipality["nome"]
            return (
                KIND_CITY,
                to_hierarchy(SOUTH_AMERICA_CODE, BRAZIL_CODE, state_id),
                to_query(
                    {KIND_COUNTRY: BRAZIL_CODE, KIND_STATE: state_id},
                    {
                        KIND_COUNTRY: BRAZIL_CODE,
                        KIND_STATE: state_id,
                        KIND_MESOREGION: mesoregion_id,
                    },
                    {
                        KIND_COUNTRY: BRAZIL_CODE,
                        KIND_STATE: state_id,
                        KIND_MESOREGION: microregion_id,
                    },
                ),
                municipality["id"],
                name,
                name,
                None,
                None,
            )

        fetch("localidades/municipios", "7_municipios.csv", row)


def fetch(url_path, csv_file_name, row_fn):
    r = requests.get(BASE_URL + url_path)
    if r.status_code == 200:
        with open(CSV_DIR / csv_file_name, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(HEADER)
            for item in r.json():
                writer.writerow(row_fn(item))
    else:
        raise Exception(f"Failed to request {url}\n{r.text}")


def to_hierarchy(*codelist):
    return ":".join(codelist)


def to_query(*dictlist):
    queries = []
    for d in dictlist:
        query = []
        for k, v in d.items():
            query.append(f"{k}={v}")
        queries.append("&".join(query))
    return ";".join(queries)
