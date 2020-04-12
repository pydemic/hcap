import random
from types import MappingProxyType as frozendict
from typing import Union

from faker import Factory

from locations.fake import random_state, random_city
from .models import User

fake = Factory.create("pt-BR")


def create_user(email=None, password=None, validate_email=True, force=False, **kwargs):
    """
    Generic function for creating users.

    It creates a user, sets password and register e-mail in allauth.
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
        "state": kwargs.get("state") or random_state(),
        **kwargs,
    }
    user = User(**kwargs)
    user.set_password(password)
    user.save()
    if validate_email:
        verify_email(user)
    return user, new


def create_notifier(suffix: Union[str, int] = "", is_authorized=True, **kwargs):
    state = kwargs.setdefault("state", random_state())
    unit = healthcare_unit(city=random_city(state))
    dash_idx = f"-{suffix}" if suffix != "" else ""
    kwargs = {
        "email": f"notifier{dash_idx}@notifier.com",
        "password": "notifier",
        "name": f"Joe Notifier Smith {suffix}".strip(),
        "is_authorized": is_authorized,
        "role": User.ROLE_NOTIFIER,
        **kwargs,
    }
    user, is_new = create_user(**kwargs)
    user.healthcare_unit_ = unit
    unit.register_notifier(user, authorize=is_authorized)
    return user, is_new


def create_manager(notifiers=None, **kwargs):
    """
    Create manager. If notifiers is given and is a tuple (a, b), it generates
    a authorized notifiers and b non-authorized notifiers in the same state.
    """
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

    # Create a authorized and b non-authorized notifiers in the same state
    if notifiers:
        a, b = notifiers
        kwargs_a = {"state": state, "is_authorized": True}
        kwargs_b = {**kwargs_a, "is_authorized": False}
        user.notifiers = [
            *(create_notifier(i, **kwargs_a)[0] for i in range(a)),
            *(create_notifier(i, **kwargs_b)[0] for i in range(a, b + a)),
        ]
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
        "city": kwargs.get("city") or random_city(),
        "name": "Foo Bar Hospital",
        **kwargs,
    }
    return HealthcareUnit.objects.create(**kwargs)
