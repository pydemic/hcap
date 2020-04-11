from django import forms
from .validators import existing_cnes_validator


class CNESForm(forms.Form):
    cnes = forms.CharField(
        label="Número de CNES",
        max_length=20,
        help_text="Digite o número de CNES da unidade da qual você é o notificador.",
        validators=[existing_cnes_validator],
    )

    def save(self, user):
        nes = self.cleaned_data["cnes"]


class FillCitiesForm(forms.Form):
    cities = forms.CharField(
        label="Lista de municípios do gestor regional",
        help_text="Inclua um município por linha e dê preferência a usar o código IBGE ao invés do nome de cada município.",
        widget=forms.Textarea,
    )
    state_manager = forms.BooleanField(label="Gestor estadual?")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
