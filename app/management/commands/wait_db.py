import time

import psycopg2
from django.conf import settings
from django.core.management.base import CommandError

from project.management import BaseCommand


class Command(BaseCommand):
    help = "Continously check PostgreSQL connection"

    waiting = 1  # seconds
    next_waiting = 1  # seconds
    max_waiting = 20  # seconds

    attempts = 0
    max_attempts = None  # None = Indefinitely

    database_name = None
    database_user = None
    database_password = None
    database_host = None
    database_port = None

    ready = False
    more_attempts = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-attempts",
            nargs="?",
            type=int,
            help="Maximum attempts to be performed. If not set, it will attempt indefinitely",
        )

        parser.add_argument(
            "--max-waiting",
            nargs="?",
            type=int,
            default=20,
            help="Maximum waiting, in seconds, between attempts",
        )

    def safe_handle(self, *args, **options):
        if settings.DATABASE_TYPE == "postgresql":
            self.max_attempts = options["max_attempts"]
            self.max_waiting = options["max_waiting"]

            database_settings = settings.DATABASES["default"]
            self.database_name = database_settings["NAME"]
            self.database_user = database_settings["USER"]
            self.database_password = database_settings["PASSWORD"]
            self.database_host = database_settings["HOST"]
            self.database_port = database_settings["PORT"]

            self.inform("Checking PostgreSQL connection", topic=True)
            self.inform("Connection... ", depth=1, ending="")

            while self.more_attempts:
                self.check_postgres()

                if self.ready:
                    self.more_attempts = False
                else:
                    self.inform(self.style.NOTICE("FAILED"))
                    self.check_attempts()

            if self.ready:
                self.inform(self.style.SUCCESS("OK"))
            else:
                data_message = " ".join(
                    [
                        f"host={self.database_host}",
                        f"port={self.database_port}",
                        f"database={self.database_name}",
                        f"user={self.database_user}",
                        "password=[FILTERED]",
                    ]
                )

                raise CommandError(f"Failed to connect: {data_message}")
        else:
            self.inform("Database is not PostgreSQL, skipping...")

    def check_postgres(self):
        self.attempts += 1
        try:
            psycopg2.connect(
                database=self.database_name,
                user=self.database_user,
                password=self.database_password,
                host=self.database_host,
                port=self.database_port,
            ).close()
            self.ready = True
        except psycopg2.OperationalError:
            self.ready = False

    def is_max_attempts_reached(self):
        return (self.max_attempts is not None) and (self.attempts > self.max_attempts)

    def check_attempts(self):
        if self.max_attempts is None or self.attempts <= self.max_attempts:
            self.maybe_print_attempt()
            time.sleep(self.waiting)
            self.update_waiting()
        else:
            self.more_attempts = False

    def update_waiting(self):
        if self.waiting != self.max_waiting:
            if self.next_waiting < self.max_waiting:
                self.waiting, self.next_waiting = [
                    self.next_waiting,
                    self.waiting + self.next_waiting,
                ]
            else:
                self.waiting = self.max_waiting

    def maybe_print_attempt(self):
        if self.max_attempts is None:
            summary = f"[{self.attempts}]"
        else:
            summary = f"[{self.attempts}/{self.max_attempts}]"

        self.inform(f"{summary} Retrying in {self.waiting} second(s)... ", depth=1, ending="")
