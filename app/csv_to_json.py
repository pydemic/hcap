"""
Code to specifically convert tbEstabelecimento2020
into a more useful and filtered json
be careful with reuse.
"""
import csv
import json
from pathlib import Path


def convert_csv_to_json(csv_file, json_file):
    data = {}
    indent = None

    with open(csv_file) as csv_file:
        csvReader = csv.DictReader(csv_file, delimiter=";")
        fields = {
            "CO_CNES": "cnes_id",
            "NO_FANTASIA": "name",
            "CO_MUNICIPIO_GESTOR": "city_id",
        }
        for row in csvReader:
            get_fields_data(row, data, fields)

    with open(json_file, "w") as json_file:
        json_file.write(json.dumps(data, indent=indent))


def get_all_data(row, data):
    unidade = row["CO_UNIDADE"]
    data[unidade] = row


def get_fields_data(row, data, fields):
    unidade = row["CO_UNIDADE"]
    filtered = {}
    if row["TP_UNIDADE"] in ["05", "07" "77", "5", "7", "005", "007", "077"]:
        for field in fields.keys():
            filtered[fields[field]] = row[field]

        data[unidade] = filtered


if __name__ == "__main__":
    cnes_path = Path(__file__).parent / "data"
    convert_csv_to_json(
        cnes_path / "tbEstabelecimento202002.csv", cnes_path / "estabelecimentos_filtrados.json"
    )
