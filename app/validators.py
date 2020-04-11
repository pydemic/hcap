from django.core.exceptions import ValidationError

from . import models


def existing_cnes_validator(cnes):
    if not models.HealthcareUnit.objects.filter(cnes_id=cnes).exists():
        raise ValidationError("Não encontrou unidade hospitalar com o número de CNES indicado.")
