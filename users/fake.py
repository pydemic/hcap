import random
from types import MappingProxyType as frozendict

from faker import Factory

from .models import User

fake = Factory.create("pt-BR")


def create_admin(**kwargs):
    kwargs = {
        "password": "user",
        "name": "Maurice Moss",
        "email": "admin@admin.com",
        "role": User.ROLE_MANAGER,
        "is_authorized": True,
        "is_superuser": True,
        **kwargs,
    }
    return create_user(**kwargs)


def create_default_user(**kwargs):
    kwargs = {
        "email": "user@user.com",
        "password": "user",
        "name": "Joe User Smith",
        "is_authorized": True,
        **kwargs,
    }
    return create_user(**kwargs)


def create_notifier(**kwargs):
    kwargs = {
        "email": "notifier@notifier.com",
        "password": "notifier",
        "name": "Joe Notifier Smith",
        "is_authorized": True,
        "role": User.ROLE_NOTIFIER,
        **kwargs,
    }
    return create_user(**kwargs)


def create_manager(**kwargs):
    kwargs = {
        "email": "manager@manager.com",
        "password": "manager",
        "name": "Joe Manager Smith",
        "is_authorized": True,
        **kwargs,
    }
    return create_user(**kwargs)


def create_user(email=None, password=None, validate_email=True, **kwargs):
    """
    Generic function for creating users.

    It creates user, sets password and register e-mail in allauth.
    """
    try:
        return User.objects.get(email=email), False
    except User.DoesNotExist:
        kwargs = {
            "cpf": kwargs.get("cpf") or random_cpf(),
            "name": kwargs.get("name") or fake.name(),
            **kwargs,
        }
        email = email or fake.email()
        user = User.objects.create_user(email, password or fake.password(), **kwargs)
        if validate_email:
            verify_email(user)
        return user, True


def verify_email(user):
    email, _ = user.emailaddress_set.update_or_create(email=user.email, verified=True)
    email.set_as_primary()
    return email


def random_cpf():
    """Return a random valid CPF."""
    n = [random.randrange(10) for i in range(9)]

    # 1st digit of verification code
    sum_ = sum(x * y for x, y in zip(n, range(10, 1, -1)))
    n.append((11 - sum_ % 11) % 10)

    # 2nd digit of verification code
    sum_ = sum(x * y for x, y in zip(n, range(11, 1, -1)))
    n.append((11 - sum_ % 11) % 10)

    return "%d%d%d.%d%d%d.%d%d%d-%d%d" % tuple(n)


def random_set(fn, size, blocked=(), max_tries=25, args=(), kwargs=frozendict({})):
    """
    Call fn multiple times to generate a set of random unique values with the
    given size.

    Optionally, items included in the blocked set will not be included in the
    output.
    """
    res = set()
    blocked = set(blocked)
    while len(res) < size:
        for _ in range(max_tries):
            new = fn(*args, **kwargs)
            if new not in blocked and new not in res:
                res.add(new)
    return res
