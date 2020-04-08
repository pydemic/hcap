import os
from invoke import task


# Database


@task
def db(ctx):
    """Make migrations and then migrate."""
    ctx.run("python manage.py makemigrations")
    ctx.run("python manage.py migrate")


@task
def migrate(ctx):
    """Alias to Django's "migrate" command."""
    ctx.run("python manage.py migrate")


@task
def migrations(ctx):
    """Alias to Django's "makemigrations" command."""
    ctx.run("python manage.py makemigrations")


# Development


@task
def run(ctx):
    """Alias to Django's "runserver" command."""
    ctx.run("python manage.py runserver")


@task
def test(ctx):
    ctx.run("black --check .")
    ctx.run("pycodestyle")
    ctx.run("coverage run --source='.' manage.py test")
    ctx.run("coverage report --show-missing")


# Production


@task
def collectstatic(ctx):
    ctx.run("python manage.py collectstatic --clear --no-input")


@task
def serve(ctx):
    """Migrate and serve the system using gunicorn."""
    migrate(ctx)

    port = os.environ.get("SERVER_PORT", "8000")
    workers = os.environ.get("SERVER_WORKERS", "1")

    ctx.run(f"gunicorn project.wsgi -w {workers} -b 0.0.0.0:{port}")
