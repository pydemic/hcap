from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class DateNotFromFutureValidator:
    def __call__(self, value):
        if (value - date.today()).days > 0:
            raise ValidationError(_("Cannot be a future date."))

    def __eq__(self, other):
        return isinstance(other, DateNotFromFutureValidator)
