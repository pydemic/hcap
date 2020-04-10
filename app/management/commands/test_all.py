import os
import sys

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError

from project.management import BaseCommand


def safe_run(command):
    code = os.system(command)
    if code != 0:
        raise CommandError(f"'{command}' failed")


class Command(BaseCommand):
    help = "Test code styling and coverage"

    def safe_handle(self, *args, **options):
        self.test_styling()
        self.check_postgres()
        self.test_coverage()

    def test_styling(self):
        self.inform("==[black]===================", style_func=self.style.SQL_KEYWORD)
        safe_run("black --check .")

        self.inform("==[pycodestyle]=============", style_func=self.style.SQL_KEYWORD)
        safe_run("pycodestyle")
        self.inform("Style " + self.style.SUCCESS("OK"))

    def check_postgres(self):
        self.inform("==[wait_db]=================", style_func=self.style.SQL_KEYWORD)
        call_command("wait_db", verbosity=self.verbosity, max_attempts=20, max_waiting=1)

    def test_coverage(self):
        self.inform("==[coverage run]============", style_func=self.style.SQL_KEYWORD)
        safe_run(f"coverage run manage.py test --noinput --failfast --verbosity={self.verbosity}")
        self.inform("==[coverage report]=========", style_func=self.style.SQL_KEYWORD)
        safe_run(f"coverage report --show-missing")
