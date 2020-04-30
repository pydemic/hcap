import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

CPF_REGEX = re.compile(r"^([0-9]{3})\.?([0-9]{3})\.?([0-9]{3})-?([0-9]{2})$")


@deconstructible
class CPFValidator:
    def __call__(self, value):
        m = CPF_REGEX.fullmatch(value)
        if m is None:
            raise ValidationError(_('Must be formatted as "000.000.000-00".'))

        if settings.VALIDATE_CPF:
            data = "".join(m.groups())

            if (
                len(set(value)) == 1
                or (not self.is_valid_digit(data, 9))
                or (not self.is_valid_digit(data, 10))
            ):
                raise ValidationError(_("Must be a valid CPF."))

    def __eq__(self, other):
        return isinstance(other, CPFValidator)

    def is_valid_digit(self, value, at):
        numbers = value[:at]
        weights = range(at + 1, 1, -1)

        sum = 0
        for digit, weight in zip(numbers, weights):
            sum += int(digit) * weight

        remainder = sum % 11
        if remainder < 2:
            return int(value[at]) == 0
        else:
            return int(value[at]) == (11 - remainder)
