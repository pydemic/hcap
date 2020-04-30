import os

from django.conf import settings
from django.core.management import call_command

from hcap_utils.contrib.management import BaseCommand


class Command(BaseCommand):
    help = "Start hcap"

    def safe_handle(self, *args, **options):
        env = settings.ENV
        if env == "prod":
            self.start_production()
        elif env == "staging":
            self.start_staging()
        else:
            self.start_development()

    def start_development(self):
        self.compile_messages()
        self.collect_static()
        self.check_postgres()
        self.migrate()
        self.seed_development_data()
        self.runserver()

    def start_staging(self):
        self.check_postgres()
        self.migrate()
        self.seed_staging_data()
        self.start_gunicorn()

    def start_production(self):
        self.check_postgres()
        self.migrate()
        self.seed_production_data()
        self.start_gunicorn()

    def compile_messages(self):
        self.inform("==[compilemessages]=========", style_func=self.style.SQL_KEYWORD)
        call_command("compilemessages", verbosity=self.verbosity)

    def collect_static(self):
        self.inform("==[collectstatic]===========", style_func=self.style.SQL_KEYWORD)
        call_command(
            "collectstatic",
            clear=True,
            no_input=True,
            interactive=False,
            verbosity=max(self.verbosity - 1, 0),
        )

    def check_postgres(self):
        self.inform("==[wait_db]=================", style_func=self.style.SQL_KEYWORD)
        call_command("wait_db", verbosity=self.verbosity)

    def migrate(self):
        self.inform("==[migrate]=================", style_func=self.style.SQL_KEYWORD)
        call_command("migrate", verbosity=self.verbosity)

    def seed_development_data(self):
        self.seed_staging_data()

    def seed_staging_data(self):
        self.inform("==[seed]====================", style_func=self.style.SQL_KEYWORD)
        call_command(
            "seed_base_users", context="staging", no_wait_db=True, verbosity=self.verbosity
        )
        call_command("seed_base_regions", no_wait_db=True, verbosity=self.verbosity)
        call_command("seed_base_healthcare_units", no_wait_db=True, verbosity=self.verbosity)
        call_command(
            "seed_base_region_managers",
            context="staging",
            no_wait_db=True,
            verbosity=self.verbosity,
        )
        call_command(
            "seed_base_healthcare_unit_notifiers",
            context="staging",
            no_wait_db=True,
            verbosity=self.verbosity,
        )
        call_command(
            "seed_base_healthcare_unit_capacities",
            context="staging",
            no_wait_db=True,
            verbosity=self.verbosity,
        )
        call_command(
            "seed_base_healthcare_unit_conditions",
            context="staging",
            no_wait_db=True,
            verbosity=self.verbosity,
        )

    def seed_production_data(self):
        self.inform("==[seed]====================", style_func=self.style.SQL_KEYWORD)
        call_command("seed_base_users", no_wait_db=True, verbosity=self.verbosity)
        call_command("seed_base_regions", no_wait_db=True, verbosity=self.verbosity)
        call_command("seed_base_healthcare_units", no_wait_db=True, verbosity=self.verbosity)

    def runserver(self):
        self.inform("==[runserver]===============", style_func=self.style.SQL_KEYWORD)
        os.system(
            f"WERKZEUG_DEBUG_PIN=off ./manage.py runserver_plus {settings.SERVER_HOST}:{settings.SERVER_PORT} --verbosity={self.verbosity}"
        )

    def start_gunicorn(self):
        self.inform("==[gunicorn]================", style_func=self.style.SQL_KEYWORD)
        os.system(
            f"gunicorn hcap.wsgi -w {settings.SERVER_WORKERS} -b {settings.SERVER_HOST}:{settings.SERVER_PORT}"
        )
