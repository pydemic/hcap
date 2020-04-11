from ..env import env

# Set default admin password when using createfakeusers command
FAKE_ADMIN_PASSWORD = env("HCAP__FAKE_ADMIN_PASSWORD", default="admin")

# Set default user password when using createfakeusers command
FAKE_USER_PASSWORD = env("HCAP__FAKE_USER_PASSWORD", default="user")
