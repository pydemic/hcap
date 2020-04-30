from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class HealthcareUnit(models.Model):
    city = models.ForeignKey(
        "hcap_geo.Region",
        verbose_name=_("city"),
        related_name="city_healthcare_units",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    state = models.ForeignKey(
        "hcap_geo.Region",
        verbose_name=_("state"),
        related_name="state_healthcare_units",
        on_delete=models.CASCADE,
        editable=False,
        help_text=_("It will be defined according to the city."),
    )

    country = models.ForeignKey(
        "hcap_geo.Region",
        verbose_name=_("country"),
        related_name="country_healthcare_units",
        on_delete=models.CASCADE,
        editable=False,
        help_text=_("It will be defined according to the state."),
    )

    cnes_id = models.CharField(
        _("CNES registry"),
        db_index=True,
        max_length=15,
        validators=(validators.RegexValidator(r"^[0-9]+$"),),
        help_text=_("Required. At most 15 digits."),
    )

    name = models.CharField(
        _("name"), max_length=150, help_text=_("Required. At most 150 characters.")
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether the healthcare unit can be used by the system."),
    )

    class Meta:
        verbose_name = _("healthcare unit")
        verbose_name_plural = _("healthcare units")
        unique_together = ("country", "cnes_id")
        ordering = ("country", "state", "city", "name")

    def __str__(self):
        return f"{self.name} ({self.cnes_id})"

    def clean_fields(self, exclude=None):
        self.state = self.city.parents.get(kind=self.city.KIND_STATE)
        self.country = self.state.parents.get(kind=self.state.KIND_COUNTRY)
        return super().clean_fields(exclude=exclude)
