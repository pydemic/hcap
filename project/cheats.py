#
# General tweaks useful for debugging. This should be enabled only if running
# in development mode
#
import os

from django.conf import settings


def to_builtins(mod, names="*"):
    import builtins
    import importlib

    mod = importlib.import_module(mod)
    if names == "*":
        names = mod.__all__
    else:
        names = names.split()

    for k in names:
        v = getattr(mod, k)
        if not hasattr(builtins, k):
            setattr(builtins, k, v)


def add_modules(mods):
    import builtins
    import importlib

    mods = mods.items() if hasattr(mods, "items") else zip(mods, mods)

    for k, v in mods:
        mod = importlib.import_module(k)
        setattr(builtins, v, mod)


_cheat = os.environ.get("CHEAT", "").lower() == "true"

if settings.ENV == "dev" and _cheat:
    import builtins

    builtins.settings = settings
    add_modules({"numpy": "np", "pandas": "pd", "matplotlib.pyplot": "plt"})
    add_modules({"datetime", "math"})
    to_builtins("project.run")
    to_builtins("pprint")
    to_builtins("IPython", "embed")
elif _cheat:
    import warnings

    warnings.warn("Are you crazy? Cheats can only be enabled in development mode ;-)")

del settings, to_builtins, add_modules
