import os

from django import setup as _setup


def start(settings="project.settings"):
    """
    Start Django based on the given settings module.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)
    os.environ.setdefault("DJANGO_SECRET_KEY", "1234")
    os.environ.setdefault("HCAP_ENV", "dev")
    _setup()

    from django.conf import settings

    if settings.ALLOWED_HOSTS != "*":
        settings.ALLOWED_HOSTS.append("testserver")


def run(func, *args, **kwargs):
    """
    Starts Django and run function with the remaining arguments.
    """
    start()
    func(*args, **kwargs)
