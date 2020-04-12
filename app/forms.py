from django import forms
from django.contrib.auth import get_user_model

from . import models
from locations import models as location_models
from .validators import existing_cnes_validator


class CNESForm(forms.Form):
    cnes = forms.CharField(
        label="Número de CNES",
        max_length=20,
        help_text="Digite o número de CNES da unidade da qual você é o notificador.",
        validators=[existing_cnes_validator],
    )

    def save(self, user):
        cnes = self.cleaned_data["cnes"]
        unit = models.HealthcareUnit.objects.get(cnes_id=cnes)
        models.associate_notifier(user, unit)


class FillCitiesForm(forms.Form):
    cities = forms.CharField(
        label="Lista de municípios do gestor regional",
        help_text="Inclua um município por linha e dê preferência a usar o código IBGE "
        "ao invés do nome de cada município.",
        required=False,
        widget=forms.Textarea,
    )
    state_manager = forms.BooleanField(label="Gestor estadual?", required=False)

    def clean(self):
        cities = self.cleaned_data.get("cities")
        state_manager = self.cleaned_data.get("state_manager")

        if not cities and not state_manager:
            raise forms.ValidationError("Preencha ao menos um dos campos.")

        return self.cleaned_data

    def save(self, user):
        if self.cleaned_data.get("state_manager"):
            qs = location_models.City.objects.filter(state=user.state)
            for city in qs:
                location_models.associate_manager_city(user, city)
        else:
            cities = self.cleaned_data["cities"]
            for c in cities.split(","):
                try:
                    city_id = int(c)
                    city = location_models.City.objects.get(id=city_id)
                    location_models.associate_manager_city(user, city)
                except ValueError:
                    city_name = c.title()
                    city = location_models.City.objects.get(name=city_name)
                    location_models.associate_manager_city(user, city)


class NotifierPendingApprovalForm(forms.ModelForm):
    class Meta:
        model = models.NotifierForHealthcareUnit
        fields = ("notifier", "unit", "is_approved")

    def save(self, commit=True):
        obj = super().save(commit)
        if obj.is_approved and not obj.notifier.is_authorized:
            obj.notifier.is_authorized = True
            obj.notifier.save()
        return obj

    def __init__(self, manager=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if manager is not None:
            self.fields["notifier"].queryset = get_user_model().objects.filter(
                state_id=manager.state_id, role=get_user_model().ROLE_NOTIFIER
            )
            self.fields["unit"].queryset = models.HealthcareUnit.objects.filter(
                city__state_id=manager.state_id
            )
