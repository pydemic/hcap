from functools import partial
from random import randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models.aggregates import Count
from faker import Factory

from app.models import HealthcareUnity, Capacity, LogEntry
from locations.models import Municipality

User = get_user_model()


class Command(BaseCommand):
    help = "create fake app data"

    def handle(self, *files, **options):
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


def random_objects(qs, size=None):
    if size is None:
        return random_objects(qs, 1)[0]

    count = qs.aggregate(count=Count("id"))["count"]
    return [qs[randint(0, count - 1)] for _ in range(size)]


random_municipality = partial(random_objects, Municipality.objects.all())
random_user = partial(random_objects, User.objects.all())
