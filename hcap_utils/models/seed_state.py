from django.db import models
from django.utils.translation import ugettext_lazy as _


class SeedState(models.Model):
    app = models.CharField(_("app name"), max_length=30)
    model = models.CharField(_("model name"), max_length=30)

    context = models.CharField(_("seed context"), blank=True, default="default", max_length=30)
    kind = models.CharField(_("seed type"), blank=True, default="base", max_length=30)

    seeded = models.BooleanField(_("seeded"), blank=True, default=False)

    seeded_at = models.DateTimeField(_("date of seeding"), auto_now=True, editable=False)

    class Meta:
        verbose_name = _("seed state")
        verbose_name_plural = _("seed states")
        unique_together = ("app", "model", "kind")

    def __str__(self):
        return f"{self.app} {self.model} {self.kind}"
