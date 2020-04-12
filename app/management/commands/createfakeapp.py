from django.contrib.auth import get_user_model

from app import fake
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

    def handle(self, unities, scenario, **kwargs):
        self.inform("Creating fake healthcare units", topic=True)
        if unities:
            for _ in range(unities):
                fake.create_unit()
            self.inform(f"Created {unities} fake healthcare units", depth=1)

        if scenario:
            self.handle_scenario()

    def handle_scenario(self):
        try:
            notifier = User.objects.get(email="notifier@notifier.com")
            unit = notifier.healthcare_units.first() or fake.create_unit()
            unit.register_notifier(notifier)
        except User.DoesNotExist:
            self.inform("Error: notifier does not exists")
            return

        res = fake.notification_scenario((7, 7, 7, 7), unit=unit, notifier=notifier)
        n = len(res.notifications)
        cnes = unit.cnes_id
        self.inform(f"Created {n} notifications for unit with CNES id {cnes}")
