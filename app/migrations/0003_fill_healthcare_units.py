import json
from pathlib import Path

from django.db import migrations


def fill_healthcare_units(apps, schema_editor):
    HealthcareUnit = apps.get_model("app", "HealthcareUnity")
    with open(Path(__file__).parent.parent / "data" / "healthcare_units.json") as fd:
        data = json.load(fd)
    healthcare_units = [HealthcareUnit(**data[st]) for st in data]
    HealthcareUnit.objects.bulk_create(healthcare_units)


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_auto_20200409_1825"),
        ("locations", "0002_fill_states_and_cities"),
    ]

    operations = [
        migrations.RunPython(fill_healthcare_units),
    ]
