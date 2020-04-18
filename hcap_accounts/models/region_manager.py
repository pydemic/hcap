from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class RegionManager(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="region_managers",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    region = models.ForeignKey(
        "hcap_geo.Region",
        verbose_name=_("region"),
        related_name="managers",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    is_authorized = models.BooleanField(
        _("authorized"),
        default=True,
        help_text=_("Designates whether the user can manage the region."),
    )

    class Meta:
        verbose_name = _("region manager")
        verbose_name_plural = _("region managers")
        unique_together = ("user", "region")

    def __str__(self):
        return f"{self.region}: {self.user}"
