from random import random, choice, randint
from django.db.models.aggregates import Count
from django.core.management.base import BaseCommand
from faker import Factory
from app.models import HealthcareUnity, Capacity, LogEntry
from app.fields import HospitalBedsField
from locations.models import Municipality


class Command(BaseCommand):
    help = "create fake app data"

    def handle(self, *files, **options):
        health_units_created = 0
        desired_units = 10
        desired_capacities = 3
        desired_entries = 2
        fake = Factory.create("en-US")

        for _ in range(desired_units):
            health_unit = HealthcareUnity.objects.create(
                municipality=random_municipality(),
                cnes_id=fake.building_number(),
                is_active=fake.boolean(),
                name=fake.name(),
            )
            for _ in range(desired_capacities):
                Capacity.objects.create(
                    unity=health_unit,
                    date=fake.date(),
                    beds_adults=fake.random_int(),
                    beds_pediatric=fake.random_int(),
                    icu_adults=fake.random_int(),
                    icu_pediatric=fake.random_int(),
                )
            for _ in range(desired_entries):
                LogEntry.objects.create(
                    unity=health_unit,
                    date=fake.date(),
                    sari_cases_adults=fake.random_int(),
                    covid_cases_adults=fake.random_int(),
                    sari_cases_pediatric=fake.random_int(),
                    covid_cases_pediatric=fake.random_int(),
                    icu_sari_cases_adults=fake.random_int(),
                    icu_covid_cases_adults=fake.random_int(),
                    icu_sari_cases_pediatric=fake.random_int(),
                    icu_covid_cases_pediatric=fake.random_int(),
                    regular_cases_adults=fake.random_int(),
                    regular_cases_pediatric=fake.random_int(),
                    regular_icu_adults=fake.random_int(),
                    regular_icu_pediatric=fake.random_int(),
                )

        print(f"Created {desired_units} fake healthcare units")


def random_municipality():
    count = Municipality.objects.aggregate(count=Count("id"))["count"]
    random_index = randint(0, count - 1)
    return Municipality.objects.all()[random_index]
