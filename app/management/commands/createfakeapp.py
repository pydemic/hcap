import datetime
import random
from functools import partial
from random import randint

from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count
from django.utils.timezone import now
from faker import Factory

from app.models import HealthcareUnit, Capacity, LogEntry
from locations.models import Municipality
from project.management import BaseCommand

User = get_user_model()
SMALL_INT_LIMIT = 32760


class Command(BaseCommand):
    help = "Create fake app data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--unities", dest="unities", help="Number of healthcare unities to create"
        )

    def handle(self, unities, **kwargs):
        self.inform("Creating fake healthcare units", topic=True)

        n = unities = unities or 10
        try:
            user = User.objects.get(email="user@user.com")
            self.create_unit(user)
            n -= 1
        except User.DoesNotExist:
            pass
        for _ in range(n):
            self.create_unit()

        unities = self.style.SUCCESS(str(unities))
        self.inform(f"Created {unities} fake healthcare units", depth=1)

    def create_unit(self, notifier=None):
        fake = Factory.create("en-US")
        day = datetime.timedelta(days=1)
        unit = HealthcareUnit.objects.create(
            municipality=random_municipality(),
            cnes_id=fake.building_number(),
            is_active=fake.boolean(),
            name=fake.name(),
        )
        notifier = notifier or random_user()
        kwargs = {"notifier": notifier, "unit": unit}

        date = now()
        size = random.choice([10, 50, 100, 200, 500, 1000, 5000, 10000])
        n_days = lambda: random.choice([1, 2, 3, 5, 10])

        ns = distribute_beds(size)
        walker = Walker(*ns)
        self.create_capacity(date, *ns, **kwargs)
        for _ in range(n_days()):
            self.create_log_entry(date, walker, **kwargs)
            date += day

        for _ in range(n_days()):
            size = int(size * random.choice([1.05, 1.25, 1.5, 2.0]))
            ns = distribute_beds(size)
            self.create_capacity(date, *ns, **kwargs)
            for _ in range(n_days()):
                self.create_log_entry(date, walker, **kwargs)
                date += day

    def create_log_entry(self, date, walker, unit, notifier):
        kwargs = walker.next()
        return LogEntry.objects.create_clean(unit=unit, notifier=notifier, date=date, **kwargs)

    def create_capacity(self, date, a, b, c, d, unit, notifier):
        assert a >= 0 and b >= 0 and c >= 0 and d >= 0, (a, b, c, d)
        return Capacity.objects.create_clean(
            unit=unit,
            notifier=notifier,
            date=date,
            beds_adults=min(a, SMALL_INT_LIMIT),
            beds_pediatric=min(b, SMALL_INT_LIMIT),
            icu_adults=min(c, SMALL_INT_LIMIT),
            icu_pediatric=min(d, SMALL_INT_LIMIT),
        )


def distribute_beds(n):
    """
    Distribute n beds into bins of beds_adult, beds_pediatric, icu_adult,
    icu_pediatric.
    """

    r = min(0.05 + random.expovariate(0.1), 0.5)
    icu = int(r * n)
    beds = n - icu

    r = min(0.2 + random.expovariate(0.2), 0.6)
    a = int(r * beds)
    b = beds - a

    r = min(0.2 + random.expovariate(0.2), 0.6)
    c = int(r * icu)
    d = icu - c
    return a, b, c, d


class Walker:
    def __init__(self, bed, bed_p, icu, icu_p):
        self.bed = bed
        self.bed_p = bed_p
        self.icu = icu
        self.icu_p = icu_p
        self.sari = 0.15
        self.covid = 0.01
        self.overload = 0.7

    def next(self):
        def distrib(n, r):
            a = int(n * r)
            return a, n - a

        self.sari = min(0.95, self.sari * random.uniform(0.8, 1.1) + 0.1)
        self.covid = min(0.95, self.covid * random.uniform(0.8, 1.1) + 0.005)
        self.overload = max(min(0.5, self.covid * random.uniform(0.8, 1.2) + 0.05), 2.0)
        fn = lambda x: int(self.overload * x)

        sari_cases_adults, regular_cases_adults = distrib(fn(self.bed), self.sari)
        sari_cases_pediatric, regular_cases_pediatric = distrib(fn(self.bed_p), self.sari)
        icu_sari_cases_adults, icu_regular_adults = distrib(fn(self.icu), self.sari)
        icu_sari_cases_pediatric, icu_regular_pediatric = distrib(fn(self.icu_p), self.sari)

        covid_cases_adults = int(self.covid * sari_cases_adults)
        covid_cases_pediatric = int(self.covid * sari_cases_pediatric)
        icu_covid_cases_adults = int(self.covid * icu_sari_cases_adults)
        icu_covid_cases_pediatric = int(self.covid * icu_sari_cases_pediatric)

        return dict(
            sari_cases_adults=min(sari_cases_adults, SMALL_INT_LIMIT),
            covid_cases_adults=min(covid_cases_adults, SMALL_INT_LIMIT),
            sari_cases_pediatric=min(sari_cases_pediatric, SMALL_INT_LIMIT),
            covid_cases_pediatric=min(covid_cases_pediatric, SMALL_INT_LIMIT),
            icu_sari_cases_adults=min(icu_sari_cases_adults, SMALL_INT_LIMIT),
            icu_covid_cases_adults=min(icu_covid_cases_adults, SMALL_INT_LIMIT),
            icu_sari_cases_pediatric=min(icu_sari_cases_pediatric, SMALL_INT_LIMIT),
            icu_covid_cases_pediatric=min(icu_covid_cases_pediatric, SMALL_INT_LIMIT),
            regular_cases_adults=min(regular_cases_adults, SMALL_INT_LIMIT),
            regular_cases_pediatric=min(regular_cases_pediatric, SMALL_INT_LIMIT),
            icu_regular_adults=min(icu_regular_adults, SMALL_INT_LIMIT),
            icu_regular_pediatric=min(icu_regular_pediatric, SMALL_INT_LIMIT),
        )


def random_objects(qs, size=None):
    if size is None:
        return random_objects(qs, 1)[0]

    count = qs.aggregate(count=Count("id"))["count"]
    return [qs[randint(0, count - 1)] for _ in range(size)]


random_municipality = partial(random_objects, Municipality.objects.all())
random_user = partial(random_objects, User.objects.all())
