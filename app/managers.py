from django.db import models


class HealthcareUnityQuerySet(models.QuerySet):
    def for_user(self, user):
        return user.healthcare_unities.all()


class LogEntryQuerySet(models.QuerySet):
    def for_user(self, user):
        return user.healthcare_unities.all()


class CapacityQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user.all())


HealthcareUnityManager = models.Manager.from_queryset(HealthcareUnityQuerySet)
LogEntryManager = models.Manager.from_queryset(LogEntryQuerySet)
CapacityManager = models.Manager.from_queryset(CapacityQuerySet)