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
    ctx.run("python manage.py createfakeusers --admin --roles")
    ctx.run("python manage.py createfakeapp --scenario")


@task
def db_staging(ctx):
    """Populate with staging data."""
    ctx.run("python manage.py migrate")
    ctx.run("python manage.py createfakeusers --staging")
    ctx.run("python manage.py createfakeapp --staging")


@task
def migrate(ctx):
    """Alias to Django's "migrate" command."""
    ctx.run("python manage.py migrate")


@task
def migrations(ctx):
    """Alias to Django's "makemigrations" command."""
    ctx.run("python manage.py makemigrations")


#
# Server
#


@task
def collectstatic(ctx):
    ctx.run("python manage.py collectstatic --clear --no-input")


@task
def run(ctx):
    """Alias to Django's "runserver" command."""
    ctx.run("python manage.py start")


#
# Development
#


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


@task
def test(ctx):
    ctx.run("python manage.py test_all")


@task
def shell(ctx):
    ctx.run("python manage.py shell", pty=True)
