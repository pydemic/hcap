from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    code = models.CharField(
        _("code"),
        max_length=30,
        help_text=_(
            "Required. At most 30 characters."
            + " Prioritize official code from government or geographic institution."
        ),
    )

    parents = models.ManyToManyField(
        "Region",
        verbose_name=_("Parent regions"),
        related_name="children",
        help_text=_("Each region from which is part."),
    )

    parent_hierarchy = models.CharField(
        _("Default parent hierarchy"),
        max_length=180,
        blank=True,
        null=True,
        help_text=_(
            "At most 180 characters. Identifier to simplify filtering."
            + ' Set each level as the region code, separated by ":" character.'
        ),
    )

    (
        KIND_NONE,
        KIND_WORLD,
        KIND_CONTINENT,
        KIND_COUNTRY,
        KIND_MACROREGION,
        KIND_STATE,
        KIND_MESOREGION,
        KIND_CITY,
        KIND_NEIGHBORHOOD,
    ) = range(9)

    KIND_CHOICES = (
        (KIND_NONE, _("None")),
        (KIND_WORLD, _("World")),
        (KIND_CONTINENT, _("Continent")),
        (KIND_COUNTRY, _("Country")),
        (KIND_MACROREGION, _("Macroregion")),
        (KIND_STATE, _("State")),
        (KIND_MESOREGION, _("Mesoregion")),
        (KIND_CITY, _("City")),
        (KIND_NEIGHBORHOOD, _("Neighborhood")),
    )

    kind = models.PositiveSmallIntegerField(
        _("type"),
        choices=KIND_CHOICES,
        default=KIND_NONE,
        help_text=_("Required. The region type according to the hierarchy of geographic regions."),
    )

    name = models.CharField(
        _("name"), max_length=150, help_text=_("Required. At most 150 characters.")
    )

    abbr = models.CharField(
        _("name abbreviation"), max_length=100, blank=True, help_text=_("At most 100 characters.")
    )

    lat = models.DecimalField(
        _("latitude"),
        max_digits=9,
        decimal_places=7,
        blank=True,
        null=True,
        validators=(MinValueValidator(Decimal("-90.0")), MaxValueValidator(Decimal("90.0")),),
        help_text=_(
            "Required. Must be a float number between -90 and 90, inclusive,"
            + " with maximum precision of seven digits."
        ),
    )

    lng = models.DecimalField(
        _("longitude"),
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        validators=(MinValueValidator(Decimal("-180.0")), MaxValueValidator(Decimal("180.0")),),
        help_text=_(
            "Required. Must be a float number between -180 and 180, inclusive,"
            + " with maximum precision of seven digits."
        ),
    )

    class Meta:
        verbose_name = _("region")
        verbose_name_plural = _("regions")
        ordering = ("kind", "parent_hierarchy", "abbr")
        permissions = (("fill", _("Can add regions to database")),)
        unique_together = ("kind", "parent_hierarchy", "code")

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        if self.abbr is None:
            self.abbr = self.name

        self.code = self.code.upper()

        super().clean_fields(exclude)
