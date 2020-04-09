import json
from pathlib import Path

from django.db import models


class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        permissions = [("fill", "Pode adicionar lista de estados no banco")]

    def __str__(self):
        return self.name


class Municipality(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"

    def __str__(self):
        return self.name
