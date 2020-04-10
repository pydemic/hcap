import os

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
        n_users = lambda x: 1 if x else 0
        if admin:
            users_created += n_users(create_admin(admin_password))
        if user:
            users_created += n_users(create_default_user(user_password))

        # Create state_manager users
        for _ in range(state_manager):
            username = usernames.pop()
            user = User.objects.create_user(
                name=fake.name(),
                cpf=cpfs.pop(),
                email=username + "@" + fake.domain_name(),
                is_verified_notifier=True,
                is_state_manager=True,
                is_staff=True,
            )
            verify_email(user)
            users_created += 1

        # Create regular users
        for _ in range(users):
            username = usernames.pop()
            user = User.objects.create(
                cpf=cpfs.pop(), name=fake.name(), email=username + "@" + fake.domain_name()
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


def create_admin(admin_password):
    if not User.objects.filter(email="admin@admin.com"):
        user = User.objects.create_superuser(
            cpf="888.999.888-11",
            name="Maurice Moss",
            email="admin@admin.com",
            is_state_manager=True,
            is_verified_notifier=True,
            password=admin_password or os.environ.get("FAKE_ADMIN_PASSWORD", "admin"),
        )
        print("Admin user created!")
        return user
    else:
        print("Admin user was already created!")
        return None


def create_default_user(user_password):
    if not User.objects.filter(email="user@user.com"):
        user = User.objects.create_user(
            cpf="111.111.111-11",
            name="Joe User",
            email="user@user.com",
            password=user_password or os.environ.get("FAKE_USER_PASSWORD", "user"),
        )
        verify_email(user)
        return user
    else:
        print("Default user was already created!")
        return None


def verify_email(user):
    return user.emailaddress_set.create(email=user.email, verified=True, primary=True)
