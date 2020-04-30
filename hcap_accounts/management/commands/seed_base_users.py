from django.conf import settings
from django.contrib.auth import get_user_model

from hcap_utils.contrib.management import BaseSeedCommand

CSV_DIR = settings.BASE_DIR / "hcap_accounts" / "data" / "user" / "csv"


class Command(BaseSeedCommand):
    CONTEXT_DEFAULT = "default"
    CONTEXT_STAGING = "staging"

    context_choices = (CONTEXT_DEFAULT, CONTEXT_STAGING)

    app = "accounts"
    model = "user"

    def seed(self):
        if self.context == self.CONTEXT_DEFAULT:
            self.seed_from_csv(CSV_DIR / "default")
        elif self.context == self.CONTEXT_STAGING:
            self.seed_from_csv(CSV_DIR / "staging")
        else:
            self.raise_message(f'Unknown context "{self.context}"')

    def fetch_model(self, row):
        user = get_user_model()()
        user.email = row.get("email")
        user.cpf = row.get("cpf")
        user.name = row.get("name")
        user.is_staff = bool(row.get("is_staff", "False"))
        user.is_superuser = bool(row.get("is_superuser", "False"))
        user.set_password(settings.SEED_DEFAULT_PASSWORD)
        return user

    def fetch_relations(self, user, row):
        user.emailaddress_set.create(email=user.email, verified=True, primary=True)
