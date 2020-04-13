import os

from django.conf import settings
from django.core.management import call_command

from project.management import BaseCommand


class Command(BaseCommand):
    help = "Start backend"

    def safe_handle(self, *args, **options):
        if settings.ENV == "dev":
            self.start_development()
        else:
            self.start_production()

    def start_development(self):
        self.collect_static()
        self.check_postgres()
        self.migrate()
        self.runserver()

    def start_production(self):
        self.check_postgres()
        self.migrate()
        self.start_gunicorn()

    def collect_static(self):
        self.inform("==[collectstatic]===========", style_func=self.style.SQL_KEYWORD)
        call_command("collectstatic", clear=True, no_input=True, interactive=False, verbosity=0)

    def check_postgres(self):
        self.inform("==[wait_db]=================", style_func=self.style.SQL_KEYWORD)
        call_command("wait_db", verbosity=self.verbosity)

    def migrate(self):
        self.inform("==[migrate]=================", style_func=self.style.SQL_KEYWORD)
        call_command("migrate", verbosity=self.verbosity)

    def runserver(self):
        self.inform("==[runserver]===============", style_func=self.style.SQL_KEYWORD)
        os.system(
            f"WERKZEUG_DEBUG_PIN=off ./manage.py runserver_plus {settings.SERVER_HOST}:{settings.SERVER_PORT} --verbosity={self.verbosity}"
        )

    def start_gunicorn(self):
        self.inform("==[gunicorn]================", style_func=self.style.SQL_KEYWORD)
        os.system(
            f"gunicorn project.wsgi -w {settings.SERVER_WORKERS} -b {settings.SERVER_HOST}:{settings.SERVER_PORT}"
        )
