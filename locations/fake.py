import random
from functools import lru_cache
from typing import Union, Tuple

from . import models


def random_state() -> models.State:
    """
    Return a random state.
    """
    return random.choice(states())


def random_city(state=None) -> models.City:
    """
    Return a random city. If state is given, return a city within the given state.
    """
    return random.choice(cities(state))


@lru_cache(1)
def states() -> Tuple[models.State]:
    """
    Return a tuple of all states. This list is cached, so users should not
    modify the resulting state objects.
    """
    return tuple(models.State.objects.all())


@lru_cache(256)
def cities(state=None) -> Tuple[models.City]:
    """
    Return a list of all cities. This list is cached, so users should not
    modify the resulting state objects.

    If state is given, filter cities of the given state.
    """
    if state is not None:
        state_id = normalize_state(state).id
        return tuple(c for c in cities() if c.state_id == state_id)
    return tuple(models.City.objects.select_related("state").all())


def normalize_state(state: Union[str, int, models.State]) -> models.State:
    """
    Return a State object from either an State or from code or name.
    """
    if isinstance(state, models.State):
        return state
    elif isinstance(state, int) or state.isdigit():
        return models.State.objects.get(pk=state)
    elif state.isupper():
        return models.State.objects.get(code=state)
    else:
        return models.State.objects.get(name__iexact=state)
