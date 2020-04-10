from django.contrib.auth.models import UserManager as BaseManager


class UserManager(BaseManager):
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        return super()._create_user(username or email, email, password, **extra_fields)
