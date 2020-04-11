from ..env import env

# Used by runserver or gunicorn commands
SERVER_HOST = env("HCAP__HOST", default="127.0.0.1")
SERVER_PORT = env("HCAP__PORT", default=8000)

# Used by gunicorn command
SERVER_WORKERS = env("HCAP__WORKERS", default=1)
