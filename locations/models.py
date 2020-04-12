from django.conf import settings
from django.db import models


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ("name",)
        permissions = [("fill", "Pode adicionar lista de estados no banco")]

    def __str__(self):
        return self.name

    def register_manager(self, user):
        """
        Register user as a valid manager for state.
        """
        user.is_authorized = True
        user.role = user.ROLE_MANAGER
        user.save()
        create = ManagerForMunicipality.objects.update_or_create
        for city in self.cities.all():
            create(manager=user, municipality=city)


class Municipality(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"

    def __str__(self):
        return self.name

    def register_manager(self, user):
        """
        Register user as a valid manager for state.
        """
        user.is_authorized = True
        user.role = user.ROLE_MANAGER
        user.save()
        create = ManagerForMunicipality.objects.update_or_create
        create(manager=user, municipality=self)


class ManagerForMunicipality(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="m2m_municipalities_as_manager"
    )
    municipality = models.ForeignKey(Municipality, models.CASCADE, related_name="m2m_managers")
    is_approved = models.BooleanField(default=True)

    def all_managers(self, only_approved=False):
        qs = ManagerForMunicipality.objects.filter(municipality=self.municipality)
        if only_approved:
            qs = qs.filter(is_approved=True)
        return type(self.manager).objects.filter(id__in=qs.values("manager_id"), flat=True)

    def all_municipalities(self, only_approved=False):
        qs = ManagerForMunicipality.objects.filter(manager=self.manager)
        if only_approved:
            qs = qs.filter(is_approved=True)
        return type(self.municipality).objects.filter(
            id__in=qs.values("municipality_id"), flat=True
        )


def associate_manager_municipality(user, municipality):
    ManagerForMunicipality.objects.update_or_create(manager=user, municipality=municipality)
