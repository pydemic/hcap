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
        create = ManagerForCity.objects.update_or_create
        for city in self.cities.all():
            create(manager=user, city=city)


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=50)
    full_name = property(lambda self: f"{self.name} - {self.state.code}")

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
        create = ManagerForCity.objects.update_or_create
        create(manager=user, city=self)


class ManagerForCity(models.Model):
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="m2m_municipalities_as_manager"
    )
    city = models.ForeignKey(City, models.CASCADE, related_name="m2m_managers")
    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = [("manager", "city")]

    def all_managers(self, only_approved=False):
        qs = ManagerForCity.objects.filter(city=self.city)
        if only_approved:
            qs = qs.filter(is_approved=True)
        query = type(self.manager).objects
        return query.filter(id__in=qs.values("manager_id"), flat=True)

    def all_municipalities(self, only_approved=False):
        qs = ManagerForCity.objects.filter(manager=self.manager)
        if only_approved:
            qs = qs.filter(is_approved=True)
        query = type(self.city).objects
        return query.filter(id__in=qs.values("city_id"), flat=True)


def associate_manager_city(user, city_or_cities, is_approved=False):
    """
    Associate manager user with a city or a list or queryset of cities.
    """
    if isinstance(city_or_cities, City):
        ManagerForCity.objects.update_or_create(manager=user, city=city_or_cities)
    else:
        qs = ManagerForCity.objects.filter(manager=user, city__in=city_or_cities)
        qs.update(is_approved=is_approved)
        cities = qs.values_list("city_id", flat=True)
        ManagerForCity.objects.bulk_create(
            ManagerForCity(manager=user, city_id=city, is_approved=is_approved) for city in cities
        )
