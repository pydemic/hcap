import os
from random import random, choice

from django.apps import apps
from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from faker import Factory
from users.models import User


class Command(BaseCommand):
    help = "Creates fake users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--admin", action="store_true", dest="admin", help="Create an admin@admin.com user"
        )
        parser.add_argument(
            "--admin-password",
            action="store_true",
            dest="admin_password",
            help="Sets the admin password",
        )
        parser.add_argument(
            "--user", action="store_true", dest="user", help="Create an user@user.com user"
        )
        parser.add_argument(
            "--user-password",
            action="store_true",
            dest="user_password",
            help="Sets the user password",
        )
        parser.add_argument(
            "--state-manager", type=int, default=2, help="Number of state-manager members"
        )
        parser.add_argument("--users", type=int, default=50, help="Number of regular users")

    def handle(
        self,
        *files,
        admin=False,
        admin_password=None,
        user=True,
        user_password=None,
        state_manager=2,
        users=50,
        **options,
    ):
        users_created = 0
        fake = Factory.create("en-US")
        blocked_usernames = {"admin", *User.objects.values_list("email", flat=True)}
        usernames = set()
        while len(usernames) < state_manager + users:
            username = fake.user_name()
            if username not in blocked_usernames:
                usernames.add(username)

        cpfs = set()
        while len(cpfs) < state_manager + users:
            cpf = fake_cpf(fake)
            if cpf not in cpfs:
                cpfs.add(cpf)

        # Create special users with known passwords
        if admin:
            users_created += create_admin(admin_password)
        if user:
            users_created += create_default_user(user_password)

        # Create state_manager users
        for _ in range(state_manager):
            username = usernames.pop()
            user = User.objects.create(
                username=username,
                name=fake.name(),
                cpf=cpfs.pop(),
                email=username + "@" + fake.domain_name(),
                is_verified_notifier=True,
                is_state_manager=True,
                is_staff=True,
                is_superuser=False,
            )
            verify_email(user)
            users_created += 1

        # Create regular users
        for _ in range(users):
            username = usernames.pop()
            user = User.objects.create(
                username=username,
                cpf=cpfs.pop(),
                name=fake.name(),
                email=username + "@" + fake.domain_name(),
                is_verified_notifier=False,
                is_state_manager=False,
                is_superuser=False,
            )
            verify_email(user)
            users_created += 1

        # Feedback
        print(f"Created {users_created} fake users")


def fake_cpf(fake):
    digit = lambda: str(fake.random_digit())
    three_digits = lambda: digit() + digit() + digit()
    cpf = three_digits() + "." + three_digits() + "." + three_digits() + "-" + digit() + digit()
    return cpf


def verify_email(user):
    pass
    # TODO: Magic to verify the user email with some verified=True


def create_admin(admin_password):
    if not User.objects.filter(email="admin@admin.com"):
        user = User.objects.create(
            username="admin",
            cpf="888.999.888-11",
            name="Maurice Moss",
            email="admin@admin.com",
            is_state_manager=True,
            is_verified_notifier=True,
            is_superuser=True,
        )
        verify_email(user)
        user.set_password(admin_password or os.environ.get("ADMIN_PASSWORD", "admin"))
        user.save()
        print("Admin user created!")
        return 1
    else:
        print("Admin user was already created!")
        return 0


def create_default_user(user_password):
    if not User.objects.filter(email="user@user.com"):
        user = User.objects.create(
            username="user",
            cpf="111.111.111-11",
            name="Joe User",
            email="user@user.com",
            is_state_manager=False,
            is_verified_notifier=False,
            is_superuser=False,
        )
        verify_email(user)
        user.set_password(user_password or os.environ.get("USER_PASSWORD", "user"))
        user.save()
        return 1
    else:
        print("Default user was already created!")
        return 0
