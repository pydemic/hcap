from ..env import env

# Used by runserver or gunicorn commands
SERVER_HOST = env("HC__HOST", default="127.0.0.1")
SERVER_PORT = env("HC__PORT", default=8000)

# Used by gunicorn command
SERVER_WORKERS = env("HC__WORKERS", default=1)
