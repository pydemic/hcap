import os

from invoke import task


#
# Database
#


@task
def db(ctx):
    """Make migrations and then migrate."""
    ctx.run("python manage.py makemigrations")
    ctx.run("python manage.py migrate")


@task
def db_fake(ctx):
    """Populate with fake data."""
    ctx.run("python manage.py migrate")
    ctx.run("python manage.py createfakeusers --admin --user")
    ctx.run("python manage.py createfakeapp")


@task
def migrate(ctx):
    """Alias to Django's "migrate" command."""
    ctx.run("python manage.py migrate")


@task
def migrations(ctx):
    """Alias to Django's "makemigrations" command."""
    ctx.run("python manage.py makemigrations")


#
# Development
#


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


@task
def clean(ctx, db=False, yes=False):
    import re

    auto_migration = re.compile(r"\d{4}_auto_\w+.py")

    remove_files = []
    for app in os.listdir("."):
        migrations_path = f"{app}/migrations/"
        if os.path.exists(migrations_path):
            migrations = os.listdir(migrations_path)
            if "__pycache__" in migrations:
                migrations.remove("__pycache__")
            elif sorted(migrations) == ["__init__.py", "0001_initial.py"]:
                remove_files.append(f"{migrations_path}/0001_initial.py")
            else:
                remove_files.extend(
                    [f"{migrations_path}/{f}" for f in migrations if auto_migration.fullmatch(f)]
                )

    if remove_files:
        print("Listing migrations:")
        for file in remove_files:
            print(f"* {file}")
        if yes or input("Remove those files? (y/N)").lower() == "y":
            for file in remove_files:
                os.remove(file)
    else:
        print("No auto migrations found.")

    if db:
        try:
            os.remove("db.sqlite3")
            print("Removed db.sqlite3")
        except FileNotFoundError:
            print("No sqlite db to remove")


#
# Production
#


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
