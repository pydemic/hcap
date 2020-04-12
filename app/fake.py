import datetime
import random
from collections import namedtuple
from functools import partial
from numbers import Number
from random import randint

import numpy as np
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.timezone import now
from faker import Factory

from locations.models import City
from users.fake import create_notifier
from . import models

fake = Factory.create("pt-BR")

User = get_user_model()
SMALL_INT_LIMIT = 32760
RANDOM_SIZES = [10, 50, 100, 200, 500, 1000, 5000, 10000]
NotificationScenario = namedtuple("NotificationScenario", ["capacities", "notifications"])


def create_unit():
    return models.HealthcareUnit.objects.create_clean(
        city=random_city(),
        cnes_id=str(random.randrange(1000, 1_000_000_000)),
        is_active=fake.boolean(),
        name=fake.name() + " Hospital",
    )


def create_capacity(beds_adults=100, beds_pediatric=10, icu_adults=10, icu_pediatric=0, **kwargs):
    safe = lambda x: max(0, min(x or 0, SMALL_INT_LIMIT))
    fix_unit_notifier(kwargs)
    return models.Capacity.objects.create_clean(
        beds_adults=safe(beds_adults),
        beds_pediatric=safe(beds_pediatric),
        icu_adults=safe(icu_adults),
        icu_pediatric=safe(icu_pediatric),
        **kwargs,
    )


def create_notification(
    sari_cases_adults=None,
    covid_cases_adults=None,
    sari_cases_pediatric=None,
    covid_cases_pediatric=None,
    icu_sari_cases_adults=None,
    icu_covid_cases_adults=None,
    icu_sari_cases_pediatric=None,
    icu_covid_cases_pediatric=None,
    regular_cases_adults=None,
    regular_cases_pediatric=None,
    icu_regular_adults=None,
    icu_regular_pediatric=None,
    **kwargs,
):
    safe = lambda x: max(0, min(x or 0, SMALL_INT_LIMIT))
    fix_unit_notifier(kwargs)
    return models.LogEntry.objects.create_clean(
        sari_cases_adults=safe(sari_cases_adults),
        covid_cases_adults=safe(covid_cases_adults),
        sari_cases_pediatric=safe(sari_cases_pediatric),
        covid_cases_pediatric=safe(covid_cases_pediatric),
        icu_sari_cases_adults=safe(icu_sari_cases_adults),
        icu_covid_cases_adults=safe(icu_covid_cases_adults),
        icu_sari_cases_pediatric=safe(icu_sari_cases_pediatric),
        icu_covid_cases_pediatric=safe(icu_covid_cases_pediatric),
        regular_cases_adults=safe(regular_cases_adults),
        regular_cases_pediatric=safe(regular_cases_pediatric),
        icu_regular_adults=safe(icu_regular_adults),
        icu_regular_pediatric=safe(icu_regular_pediatric),
        **kwargs,
    )


def capacity_progression(days=(7, 7, 14), size=None, expansions=None, **kwargs):
    """
    Create a progression of capacities.

    Args:
        days:
            Number of days between each expansion.
        size:
            Initial capacity size. Can be an integer with total capacity, a
            2-tuple with beds/icus and a 4-tuple of (clinic, pediatric, icu, pediatric
            icu)
        expansions:
            A sequence or a single number with the expected expansion of beds.
            If not given, it expands (or contracts) randomly.
    """
    size = size or random.choice(RANDOM_SIZES)
    fix_unit_notifier(kwargs)
    date = kwargs.pop("date", None) or now().date()

    if expansions is None:
        expansions = [random.uniform(0.9, 1.25) for _ in days]
    elif isinstance(expansions, Number):
        expansions = [expansions] * len(days)
    assert len(expansions) == len(days)

    date = date or now().date()

    def capacity(size, **extra):
        return create_capacity(*distribute_beds(size), **kwargs, **extra)

    ans = [capacity(size, date=date)]
    for step, e in zip(days, expansions):
        date += datetime.timedelta(days=step)
        size = (e * np.array(size)).astype(int)
        ans.append(capacity(size, date=date))

    return ans


def notification_progression(days=7, size=None, capacity=None, **kwargs):
    """
    Create a week (or another time-span) of daily notifications.
    """
    unit, notifier = fix_unit_notifier(kwargs)
    date = kwargs.pop("date", None) or now().date()
    if capacity is None:
        ns = distribute_beds(size)
        capacity = create_capacity(*ns, unit=unit, date=date, notifier=notifier)
    walker = CaseNotificationsWalker(**capacity.capacities)

    def notification(date, cases):
        return create_notification(date=date, **kwargs, **cases)

    ans = []
    for i in range(days):
        cases = walker.step()
        ans.append(notification(date + datetime.timedelta(i), cases))
    return ans


def notification_scenario(days=(7, 7, 14), **kwargs):
    fix_unit_notifier(kwargs)
    capacities = capacity_progression(days=days, **kwargs)

    kwargs.pop("expansions", None)
    kwargs.pop("size", None)

    notifications = []
    for period, capacity in zip(days, capacities):
        notifications.extend(notification_progression(period, capacity=capacity, **kwargs))

    return NotificationScenario(capacities, notifications)


def normalize_date(x):
    if isinstance(x, datetime.date):
        return x
    else:
        return now().date() + datetime.timedelta(days=x)


#
# Utilities
#
class CaseNotificationsWalker:
    def __init__(
        self,
        beds_adults,
        beds_pediatric,
        icu_adults,
        icu_pediatric,
        sari=0.15,
        covid=0.01,
        overload=0.7,
    ):
        self.bed = beds_adults
        self.bed_p = beds_pediatric
        self.icu = icu_adults
        self.icu_p = icu_pediatric
        self.sari = sari
        self.covid = covid
        self.overload = overload

    def step(self):
        def distrib(n, r):
            a = int(n * r)
            return a, n - a

        self.sari = min(0.95, self.sari * random.uniform(0.8, 1.1) + 0.1)
        self.covid = min(0.95, self.covid * random.uniform(0.8, 1.1) + 0.005)
        self.overload = max(min(0.5, self.covid * random.uniform(0.8, 1.2) + 0.05), 2.0)
        fn = lambda x: int(self.overload * x)

        sari_adults, regular_adults = distrib(fn(self.bed), self.sari)
        sari_pediatric, regular_pediatric = distrib(fn(self.bed_p), self.sari)
        icu_sari_adults, icu_regular_adults = distrib(fn(self.icu), self.sari)
        icu_sari_pediatric, icu_regular_pediatric = distrib(fn(self.icu_p), self.sari)

        covid_adults = int(self.covid * sari_adults)
        covid_pediatric = int(self.covid * sari_pediatric)
        icu_covid_adults = int(self.covid * icu_sari_adults)
        icu_covid_pediatric = int(self.covid * icu_sari_pediatric)

        safe = lambda x: max(0, min(x, SMALL_INT_LIMIT))
        return dict(
            sari_cases_adults=safe(sari_adults),
            covid_cases_adults=safe(covid_adults),
            sari_cases_pediatric=safe(sari_pediatric),
            covid_cases_pediatric=safe(covid_pediatric),
            icu_sari_cases_adults=safe(icu_sari_adults),
            icu_covid_cases_adults=safe(icu_covid_adults),
            icu_sari_cases_pediatric=safe(icu_sari_pediatric),
            icu_covid_cases_pediatric=safe(icu_covid_pediatric),
            regular_cases_adults=safe(regular_adults),
            regular_cases_pediatric=safe(regular_pediatric),
            icu_regular_adults=safe(icu_regular_adults),
            icu_regular_pediatric=safe(icu_regular_pediatric),
        )

    def walk(self, n):
        return [self.step() for _ in range(n)]


def distribute_beds(n):
    """
    Distribute n beds into bins of beds_adult, beds_pediatric, icu_adult,
    icu_pediatric.
    """
    if n is None:
        n = random.choice(RANDOM_SIZES)

    if not isinstance(n, (int, np.int64)):
        if len(n) == 2:
            beds, icu = n
        elif len(n) == 4:
            return tuple(n)
        else:
            raise ValueError("must be a sequence of 2 or 4 elements.")
    else:
        r = min(0.05 + random.expovariate(0.1), 0.25)
        icu = int(r * n)
        beds = n - icu

    r = min(0.1 + 0.15 * random.expovariate(1), 0.5)
    b = int(r * beds)
    a = beds - b

    r = min(0.1 + 0.15 * random.expovariate(1), 0.5)
    d = int(r * icu)
    c = icu - d
    return a, b, c, d


def fix_unit_notifier(kwargs):
    notifier = kwargs.get("notifier") or create_notifier()[0]
    unit = kwargs.get("unit")
    unit = unit or getattr(notifier, "healthcare_unit_", unit)
    unit = unit or create_unit()
    kwargs.update(notifier=notifier, unit=unit)
    return unit, notifier


def random_objects(qs, size=None):
    if size is None:
        return random_objects(qs, 1)[0]

    count = qs.aggregate(count=Count("id"))["count"]
    return [qs[randint(0, count - 1)] for _ in range(size)]


random_city = partial(random_objects, City.objects.all())
random_user = partial(random_objects, User.objects.all())
