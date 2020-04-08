from django.db import models


def HospitalBedsField(*args, **kwargs):
    """
    Default values for Hospital Beds Fields
    """
    return models.PositiveSmallIntegerField(*args, **kwargs)
