from hcap.settings.env import env

SEED_DEFAULT_PASSWORD = env("HCAP__SEED_DEFAULT_PASSWORD", default="Pass@123")
