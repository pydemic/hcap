import random

from django.contrib.auth import get_user_model

from app import fake
from app.models import HealthcareUnit, LogEntry
from project.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create fake app data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--unities", default=0, help="Number of random healthcare unities to create"
        )
        parser.add_argument(
            "--scenario", action="store_true", help="Create scenarios for default users"
        )
        parser.add_argument(
            "--random", action="store_true", help="Choose a random notifier and creates a scenario"
        )
        parser.add_argument(
            "--init-capacities",
            action="store_true",
            help="Initialize capacities for all healthcare units",
        )
        parser.add_argument(
            "--init-notifications",
            action="store_true",
            help="Initialize notifications for all healthcare units",
        )
        parser.add_argument("--staging", action="store_true", help="Create the staging database")

    def handle(
        self, unities, scenario, staging, random, init_capacities, init_notifications, **kwargs
    ):
        self.inform("Creating fake healthcare units", topic=True)
        if init_capacities:
            self.handle_init_capacities()
        elif init_notifications:
            self.handle_init_notifications()
        elif scenario:
            for _ in range(unities):
                self.handle_scenario(random)
        elif staging:
            self.handle_staging()
        elif unities:
            for _ in range(unities):
                fake.create_unit()
            self.inform(f"Created {unities} fake healthcare units", depth=1)

    def handle_scenario(self, is_random=False):
        if is_random:
            qs = User.objects.notifiers()
            idx = random.randrange(qs.count())
            notifier = qs[idx]
            days = None
        else:
            try:
                notifier = User.objects.get(email="notifier@notifier.com")
            except User.DoesNotExist:
                return
            days = 7, 7, 7, 7
        self.fill_notifier(notifier, days=days)

    def handle_staging(self):
        self.handle_scenario()
        qs = User.objects.filter(role=User.ROLE_NOTIFIER, is_authorized=True)
        qs = qs.exclude(email="notifier@notifier.com")
        for notifier in qs:
            self.fill_notifier(notifier)
        self.handle_init_capacities(0.1)
        self.handle_init_notifications(0.1)

    def handle_init_capacities(self, prob=0.01):
        for unit in HealthcareUnit.objects.filter(is_active=True):
            if random.random() < prob:
                ns = fake.distribute_beds(random.choice(fake.RANDOM_SIZES))
                fake.create_capacity(*ns, unit=unit)

    def handle_init_notifications(self, prob=0.01):
        n = LogEntry.objects.count()
        for unit in HealthcareUnit.objects.filter(is_active=True):
            if random.random() < prob:
                ns = fake.distribute_beds(random.choice(fake.RANDOM_SIZES))
                fake.create_notification(*ns, unit=unit)
        m = LogEntry.objects.count()
        self.inform(f"Created {m - n} new notifications out of {n}")

    def fill_notifier(self, notifier, days=None):
        if days is None:
            days = random_days()

        unit = notifier.healthcare_units.first() or fake.create_unit()
        unit.register_notifier(notifier)
        self.inform("Error: notifier does not exists")

        res = fake.notification_scenario(days, unit=unit, notifier=notifier)
        n = len(res.notifications)
        cnes = unit.cnes_id
        self.inform(f"Created {n} notifications for unit with CNES id {cnes}")


def random_days():
    n = random.choice((1, 2, 3, 4, 5))
    return [random.randint(2, 14) for _ in range(n)]
