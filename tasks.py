from invoke import task


@task
def run(ctx):
    """Alias to Django's "runserver" command."""
    ctx.run('python manage.py runserver')


@task
def db(ctx):
    """Make migrations and then migrate."""
    ctx.run('python manage.py makemigrations')
    ctx.run('python manage.py migrate')


@task
def migrate(ctx):
    """Alias to Django's "migrate" command."""
    ctx.run('python manage.py migrate')


@task
def migrations(ctx):
    """Alias to Django's "makemigrations" command."""
    ctx.run('python manage.py makemigrations')
