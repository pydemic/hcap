from hcap.settings.env import env

# Used by user seed commands
SEED_DEFAULT_PASSWORD = env("SEED_DEFAULT_PASSWORD", default="Pass@123")
