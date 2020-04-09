import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.conf import settings

CPFRegex = r"^[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}$"


@deconstructible
class CPFValidator:
    def __call__(self, value):
        if re.fullmatch(CPFRegex, value) is None:
            raise ValidationError(
                "CPF deve seguir a formatação xxx.xxx.xxx-xx, substituindo x por números."
            )

        value = list(re.sub(r"[^0-9]", "", value))
        if not settings.VALIDATE_CPF:
            return

        if (
            len(set(value)) == 1
            or (not self.is_valid_digit(value, 9))
            or (not self.is_valid_digit(value, 10))
        ):
            raise ValidationError("CPF deve ser válido.")

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
