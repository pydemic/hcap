from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from hcap_utils.contrib.validations import DateNotFromFutureValidator


class HealthcareUnitCondition(models.Model):
    notifier = models.ForeignKey(
        "hcap_accounts.HealthcareUnitNotifier",
        verbose_name=_("notifier"),
        related_name="condition_notifications",
        on_delete=models.CASCADE,
        help_text=_("Required."),
    )

    healthcare_unit = models.ForeignKey(
        "hcap_institutions.HealthcareUnit",
        verbose_name=_("healthcare unit"),
        related_name="condition_notifications",
        on_delete=models.CASCADE,
        editable=False,
        help_text=_("It will be defined according to the notifier."),
    )

    date = models.DateField(
        _("date"),
        default=date.today,
        db_index=True,
        help_text=_("Required. Date from which the healthcare unit changed its condition."),
        validators=(DateNotFromFutureValidator(),),
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(_("updated at"), auto_now=True, editable=False)

    # SARI/COVID adult clinical cases

    sari_adult_clinical_cases = models.PositiveSmallIntegerField(
        _("SARI adult clinical cases"),
        help_text=_(
            "Required. Includes confirmed COVID adult cases. Excludes SARI adult ICU cases."
        ),
    )

    covid_adult_clinical_cases = models.PositiveSmallIntegerField(
        _("confirmed COVID adult clinical cases"),
        help_text=_("Required. Excludes confirmed COVID adult ICU cases"),
    )

    # SARI/COVID pediatric clinical cases

    sari_pediatric_clinical_cases = models.PositiveSmallIntegerField(
        _("SARI pediatric clinical cases"),
        help_text=_(
            "Required. Includes confirmed COVID pediatric cases. Excludes SARI pediatric ICU cases."
        ),
    )

    covid_pediatric_clinical_cases = models.PositiveSmallIntegerField(
        _("confirmed COVID pediatric clinical cases"),
        help_text=_("Required. Excludes confirmed COVID pediatric ICU cases."),
    )

    # SARI/COVID adult ICU cases

    sari_adult_icu_cases = models.PositiveSmallIntegerField(
        _("SARI adult ICU cases"),
        help_text=_("Required. Includes confirmed COVID adult ICU cases."),
    )

    covid_adult_icu_cases = models.PositiveSmallIntegerField(
        _("confirmed COVID adult ICU cases"), help_text=_("Required.")
    )

    # SARI/COVID pediatric ICU cases

    sari_pediatric_icu_cases = models.PositiveSmallIntegerField(
        _("SARI pediatric ICU cases"),
        help_text=_("Required. Includes confirmed COVID pediatric ICU cases."),
    )

    covid_pediatric_icu_cases = models.PositiveSmallIntegerField(
        _("confirmed COVID pediatric ICU cases"), help_text=_("Required.")
    )

    # General clinical cases

    general_adult_clinical_cases = models.PositiveSmallIntegerField(
        _("general adult clinical cases"),
        help_text=_("Required. Excludes SARI adult clinical cases and general adult ICU cases."),
    )

    general_pediatric_clinical_cases = models.PositiveSmallIntegerField(
        _("general pediatric clinical cases"),
        help_text=_(
            "Required. Excludes SARI pediatric clinical cases and general pediatric ICU cases."
        ),
    )

    # General ICU cases

    general_adult_icu_cases = models.PositiveSmallIntegerField(
        _("general adult ICU cases"), help_text=_("Required. Excludes SARI adult ICU cases."),
    )

    general_pediatric_icu_cases = models.PositiveSmallIntegerField(
        _("general pediatric ICU cases"),
        help_text=_("Required. Excludes SARI pediatric ICU cases."),
    )

    class Meta:
        verbose_name = _("healthcare unit condition")
        verbose_name_plural = _("healthcare unit conditions")
        unique_together = ("healthcare_unit", "date")
        ordering = ("healthcare_unit", "date")

    def __str__(self):
        return f"{self.healthcare_unit}: {self.date}"

    def clean_fields(self, exclude=None):
        if "covid_adult_clinical_cases" not in exclude:
            self.covid_adult_clinical_cases = self.covid_adult_clinical_cases or 0

        if "covid_pediatric_clinical_cases" not in exclude:
            self.covid_pediatric_clinical_cases = self.covid_pediatric_clinical_cases or 0

        if "covid_adult_icu_cases" not in exclude:
            self.covid_adult_icu_cases = self.covid_adult_icu_cases or 0

        if "covid_pediatric_icu_cases" not in exclude:
            self.covid_pediatric_icu_cases = self.covid_pediatric_icu_cases or 0

        if "healthcare_unit_id" not in exclude and self.notifier is not None:
            self.healthcare_unit_id = self.notifier.healthcare_unit_id

        return super().clean_fields(exclude=exclude)

    def clean(self):
        if (
            self.updated_at is not None
            and self.created_at is not None
            and (self.updated_at - self.created_at).days > 0
        ):
            raise ValidationError(
                _("Cannot change notification after elapsed 24 hours from creation.")
            )
        else:
            errors = {}
            message = _("COVID cases cannot be greater than SARI cases.")
            if self.covid_adult_clinical_cases > self.sari_adult_clinical_cases:
                errors["covid_adult_clinical_cases"] = message

            if self.covid_pediatric_clinical_cases > self.sari_pediatric_clinical_cases:
                errors["covid_pediatric_clinical_cases"] = message

            if self.covid_adult_icu_cases > self.sari_adult_icu_cases:
                errors["covid_adult_icu_cases"] = message

            if self.covid_pediatric_icu_cases > self.sari_pediatric_icu_cases:
                errors["covid_pediatric_icu_cases"] = message

            if errors:
                raise ValidationError(errors)

    @property
    def summary(self):
        return {
            "sari_adult_clinical_cases": self.sari_adult_clinical_cases,
            "covid_adult_clinical_cases": self.covid_adult_clinical_cases,
            "sari_pediatric_clinical_cases": self.sari_pediatric_clinical_cases,
            "covid_pedidatric_clinical_cases": self.covid_pediatric_clinical_cases,
            "sari_adult_icu_cases": self.sari_adult_icu_cases,
            "covid_adult_icu_cases": self.covid_adult_icu_cases,
            "sari_pediatric_icu_cases": self.sari_pediatric_icu_cases,
            "covid_pediatric_icu_cases": self.covid_pediatric_icu_cases,
            "general_adult_clinical_cases": self.general_adult_clinical_cases,
            "general_pediatric_clinical_cases": self.general_pediatric_clinical_cases,
            "general_adult_icu_cases": self.general_adult_icu_cases,
            "general_pediatric_icu_cases": self.general_pediatric_icu_cases,
        }

    # Total properties

    @property
    def total_cases(self):
        return self.adult_cases + self.pediatric_cases

    @property
    def adult_cases(self):
        return self.sari_adult_cases + self.general_adult_cases

    @property
    def pediatric_cases(self):
        return self.sari_pediatric_cases + self.general_pediatric_cases

    @property
    def clinical_cases(self):
        return self.sari_clinical_cases + self.general_clinical_cases

    @property
    def icu_cases(self):
        return self.sari_icu_cases + self.general_icu_cases

    # SARI composite properties

    @property
    def sari_cases(self):
        return self.sari_adult_cases + self.sari_pediatric_cases

    @property
    def sari_adult_cases(self):
        return self.sari_adult_clinical_cases + self.sari_adult_icu_cases

    @property
    def sari_pediatric_cases(self):
        return self.sari_pediatric_clinical_cases + self.sari_pediatric_icu_cases

    @property
    def sari_clinical_cases(self):
        return self.sari_adult_clinical_cases + self.sari_pediatric_clinical_cases

    @property
    def sari_icu_cases(self):
        return self.sari_adult_icu_cases + self.sari_pediatric_icu_cases

    # COVID composite properties

    @property
    def covid_cases(self):
        return self.covid_adult_cases + self.covid_pediatric_cases

    @property
    def covid_adult_cases(self):
        return self.covid_adult_clinical_cases + self.covid_adult_icu_cases

    @property
    def covid_pediatric_cases(self):
        return self.covid_pediatric_clinical_cases + self.covid_pediatric_icu_cases

    @property
    def covid_clinical_cases(self):
        return self.covid_adult_clinical_cases + self.covid_pediatric_clinical_cases

    @property
    def covid_icu_cases(self):
        return self.covid_adult_icu_cases + self.covid_pediatric_icu_cases

    # General composite properties

    @property
    def general_cases(self):
        return self.general_adult_cases + self.general_pediatric_cases

    @property
    def general_adult_cases(self):
        return self.general_adult_clinical_cases + self.general_adult_icu_cases

    @property
    def general_pediatric_cases(self):
        return self.general_pediatric_clinical_cases + self.general_pediatric_icu_cases

    @property
    def general_clinical_cases(self):
        return self.general_adult_clinical_cases + self.general_pediatric_clinical_cases

    @property
    def general_icu_cases(self):
        return self.general_adult_icu_cases + self.general_pediatric_icu_cases
