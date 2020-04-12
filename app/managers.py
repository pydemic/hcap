from django.db import models
from project.managers import CleanManager


class HealthcareUnitQuerySet(models.QuerySet):
    def for_user(self, user):
        return user.healthcare_units.all()


class LogEntryQuerySet(models.QuerySet):
    def for_user(self, user):
        return user.healthcare_units.all()


class CapacityQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user.all())


HealthcareUnitManager = CleanManager.from_queryset(HealthcareUnitQuerySet)
LogEntryManager = CleanManager.from_queryset(LogEntryQuerySet)
CapacityManager = CleanManager.from_queryset(CapacityQuerySet)
