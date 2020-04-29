from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _


class HealthcareUnitCapacity(models.Model):
    notifier = models.ForeignKey(
        "hcap_accounts.HealthcareUnitNotifier",
        verbose_name=_("notifier"),
        related_name="capacity_notifications",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    healthcare_unit = models.ForeignKey(
        "hcap_institutions.HealthcareUnit",
        verbose_name=_("healthcare unit"),
        related_name="capacity_notifications",
        on_delete=models.CASCADE,
        editable=False,
        help_text=_("It will be defined according to the notifier."),
    )

    date = models.DateField(
        _("date"),
        default=date.today,
        db_index=True,
        help_text=_("Required. Date from which the healthcare unit changed its capacity."),
    )

    clinical_adult_beds = models.PositiveSmallIntegerField(
        _("clinical adult beds"), help_text=_("Required.")
    )

    clinical_pediatric_beds = models.PositiveSmallIntegerField(
        _("clinical pediatric beds"), help_text=_("Required.")
    )

    icu_adult_beds = models.PositiveSmallIntegerField(_("ICU adult beds"), help_text=_("Required."))

    icu_pediatric_beds = models.PositiveSmallIntegerField(
        _("ICU pediatric beds"), help_text=_("Required.")
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(_("updated at"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("healthcare unit capacity")
        verbose_name_plural = _("healthcare unit capacities")
        unique_together = ("healthcare_unit", "date")
        ordering = ("healthcare_unit", "date")

    def __str__(self):
        return f"{self.healthcare_unit}: {self.date}"

    @property
    def beds_summary(self):
        return {
            "clinical_adult_beds": self.clinical_adult_beds,
            "clinicial_pediatric_beds": self.clinical_pediatric_beds,
            "icu_adult_beds": self.icu_adult_beds,
            "icu_pediatric_beds": self.icu_pediatric_beds,
        }

    @property
    def total_beds(self):
        return self.total_clinical_beds + iself.total_icu_beds

    @property
    def total_clinical_beds(self):
        return self.clinical_adult_beds + self.clinical_pediatric_beds

    @property
    def total_icu_beds(self):
        return self.icu_adult_beds + self.icu_pediatric_beds

    @property
    def total_adult_beds(self):
        return self.clinical_adult_beds + self.icu_adult_beds

    @property
    def total_pediatric_beds(self):
        return self.clinical_pediatric_beds + self.icu_pediatric_beds
