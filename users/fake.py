import random
from types import MappingProxyType as frozendict

from faker import Factory

from locations.fake import random_state, random_city
from .models import User

fake = Factory.create("pt-BR")


def create_user(email=None, password=None, validate_email=True, force=False, **kwargs):
    """
    Generic function for creating users.

    It creates user, sets password and register e-mail in allauth.
    """
    new = True
    try:
        user = User.objects.get(email=email)
        if not force:
            return user, False
        else:
            user.delete()
    except User.DoesNotExist:
        pass
    kwargs = {
        "email": email or fake.email(),
        "cpf": kwargs.get("cpf") or random_cpf(),
        "name": kwargs.get("name") or fake.name(),
        "is_active": kwargs.pop("is_active", True),
        **kwargs,
    }
    user = User(**kwargs)
    user.set_password(password)
    user.save()
    if validate_email:
        verify_email(user)
    return user, new


def create_notifier(**kwargs):
    state = kwargs.setdefault("state", random_state())
    unit = healthcare_unit(municipality=random_city(state))
    kwargs = {
        "email": "notifier@notifier.com",
        "password": "notifier",
        "name": "Joe Notifier Smith",
        "is_authorized": True,
        "role": User.ROLE_NOTIFIER,
        **kwargs,
    }
    user, is_new = create_user(**kwargs)
    unit.register_notifier(user)
    return user, is_new


def create_manager(**kwargs):
    state = kwargs.setdefault("state", random_state())
    kwargs = {
        "email": "manager@manager.com",
        "password": "manager",
        "name": "Joe Manager Smith",
        "is_authorized": True,
        "role": User.ROLE_MANAGER,
        **kwargs,
    }
    user, is_new = create_user(**kwargs)
    state.register_manager(user)
    return user, is_new


def create_admin(**kwargs):
    kwargs = {
        "name": "Maurice Moss",
        "email": "admin@admin.com",
        "password": "admin",
        "role": User.ROLE_MANAGER,
        "is_authorized": True,
        "is_superuser": True,
        "is_staff": True,
        **kwargs,
    }
    return create_manager(**kwargs)


def create_default_user(**kwargs):
    kwargs = {
        "email": "user@user.com",
        "password": "user",
        "name": "Joe User Smith",
        "is_authorized": True,
        **kwargs,
    }
    return create_user(**kwargs)


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


def healthcare_unit(**kwargs) -> "app.models.HealthcareUnit":
    from app.models import HealthcareUnit

    kwargs.setdefault("is_active", True)
    obj = HealthcareUnit.objects.filter(**kwargs).first()
    if obj is not None:
        return obj
    kwargs = {
        "cnes_id": 1234,
        "municipality": kwargs.get("municipality") or random_city(),
        "name": "Foo Bar Hospital",
        **kwargs,
    }
    return HealthcareUnit.objects.create(**kwargs)
