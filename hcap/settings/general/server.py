from hcap.settings.env import env

# Used by runserver and gunicorn commands
SERVER_HOST = env("HOST", default="127.0.0.1")
SERVER_PORT = env("PORT", default=8000)

# Used by gunicorn command
SERVER_WORKERS = env("WORKERS", default=1)
