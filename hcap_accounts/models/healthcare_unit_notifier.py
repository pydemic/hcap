from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class HealthcareUnitNotifier(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="healthcare_unit_notifiers",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    healthcare_unit = models.ForeignKey(
        "hcap_institutions.HealthcareUnit",
        verbose_name=_("healthcare unit"),
        related_name="notifiers",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    is_authorized = models.BooleanField(
        _("authorized"),
        default=True,
        help_text=_("Designates whether the user can notify for the healthcare unit."),
    )

    class Meta:
        verbose_name = _("healthcare unit notifier")
        verbose_name_plural = _("healthcare unit notifiers")
        unique_together = ("user", "healthcare_unit")

    def __str__(self):
        return f"{self.healthcare_unit}: {self.user}"
