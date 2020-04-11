from django.conf import settings
from faker import Factory

from project.management import BaseCommand
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
            "--state-managers", type=int, default=2, help="Number of state-manager members"
        )
        parser.add_argument("--users", type=int, default=50, help="Number of regular users")

    def handle(
        self,
        *files,
        admin=False,
        admin_password=None,
        user=True,
        user_password=None,
        state_managers=2,
        users=50,
        **options,
    ):
        self.inform("Creating fake users", topic=True)

        users_created = 0
        fake = Factory.create("en-US")
        blocked_usernames = {"admin", "user", *User.objects.values_list("email", flat=True)}

        usernames = set()
        while len(usernames) < state_managers + users:
            username = fake.user_name()
            if username not in blocked_usernames:
                usernames.add(username)

        cpfs = set()
        while len(cpfs) < state_managers + users:
            cpf = fake_cpf(fake)
            if cpf not in cpfs:
                cpfs.add(cpf)

        # Create special users with known passwords
        n_users = lambda x: 1 if x else 0
        if admin:
            users_created += n_users(self.create_admin(admin_password))
        if user:
            users_created += n_users(self.create_default_user(user_password))

        # Create state_manager users
        for _ in range(state_managers):
            username = usernames.pop()
            user = User.objects.create_user(
                name=fake.name(),
                cpf=cpfs.pop(),
                email=username + "@" + fake.domain_name(),
                role=User.ROLE_MANAGER,
                is_authorized=True,
            )
            verify_email(user)
            users_created += 1

        # Create regular users
        for _ in range(users):
            username = usernames.pop()
            user = User.objects.create(
                cpf=cpfs.pop(),
                name=fake.name(),
                email=username + "@" + fake.domain_name(),
                role=User.ROLE_NOTIFIER,
            )
            verify_email(user)
            users_created += 1

        # Feedback
        users_created = self.style.SUCCESS(str(users_created))
        self.inform(f"Created {users_created} fake users", depth=1)

    def create_admin(self, password):
        if not User.objects.filter(email="admin@admin.com"):
            user = User.objects.create_superuser(
                cpf="888.999.888-11",
                name="Maurice Moss",
                email="admin@admin.com",
                role=User.ROLE_MANAGER,
                is_authorized=True,
            )
            user.set_password(password or settings.FAKE_ADMIN_PASSWORD)
            user.save()
            verify_email(user)
            self.inform(self.style.SUCCESS("Admin") + " user created!", depth=1)
            return user
        else:
            self.inform(self.style.WARNING("Admin") + " user was already created!", depth=1)
            return None

    def create_default_user(self, password):
        if not User.objects.filter(email="user@user.com"):
            user = User.objects.create_user(
                cpf="111.111.111-11", name="Joe User", email="user@user.com"
            )
            user.set_password(password or settings.FAKE_USER_PASSWORD)
            user.save()
            verify_email(user)
            self.inform(self.style.SUCCESS("Default") + " user created!", depth=1)
            return user
        else:
            self.inform(self.style.WARNING("Default") + " user was already created!", depth=1)
            return None


def fake_cpf(fake):
    digit = lambda: str(fake.random_digit())
    three_digits = lambda: digit() + digit() + digit()
    cpf = three_digits() + "." + three_digits() + "." + three_digits() + "-" + digit() + digit()
    return cpf


def verify_email(user):
    user.emailaddress_set.update_or_create(email=user.email, verified=True, primary=True)
