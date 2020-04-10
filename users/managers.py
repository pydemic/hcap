from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def create_user(self, email=None, password=None, state=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if state is not None:
            user.state_id = state
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_authorized", True)
        user = self.create_user(**extra_fields)
        user.emailaddress_set.create(email=user.email, verified=True, primary=True)
        return user
