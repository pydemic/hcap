"""
django-environ:
    https://django-environ.readthedocs.io/en/latest/#django-environ
"""

import environ
from pathlib import Path

ENV_PATH = Path.joinpath(Path(__file__).parent.parent.parent, ".env")

env = environ.Env()
if ENV_PATH.exists() and ENV_PATH.is_file():
    environ.Env.read_env(env_file=ENV_PATH.open())

ENV = env("HC__ENV", default="dev")
