from django.contrib.auth.models import UserManager as DjangoUserManager

from hcap_accounts.models import HealthcareUnitNotifier, RegionManager


class UserManager(DjangoUserManager):
    def create_user(self, email=None, password=None, verify_email=False, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if verify_email:
            user.emailaddress_set.create(email=user.email, verified=True, primary=True)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("verify_email", True)
        user = self.create_user(**extra_fields)
        return user

    def healthcare_unit_notifiers(healthcare_unit=None, is_authorized=None):
        queryset = HealthcareUnitNotifier.objects.all()

        if healthcare_unit is not None:
            queryset = queryset.filter(healthcare_unit=healthcare_unit)

        if is_authorized is not None:
            queryset = queryset.filter(is_authorized=is_authorized)

        ids = list(queryset.values_list("user_id", flat=True))

        return self.filter(id__in=ids)

    def region_managers(self, region=None, is_authorized=None):
        queryset = RegionManager.objects.all()

        if region is not None:
            queryset = queryset.filter(region=region)

        if is_authorized is not None:
            queryset = queryset.filter(is_authorized=is_authorized)

        ids = list(queryset.values_list("user_id", flat=True))

        return self.filter(id__in=ids)
