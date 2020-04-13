import re
from operator import attrgetter

from django import forms
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from locations.models import City, associate_manager_city
from . import models
from .validators import existing_cnes_validator


class CNESForm(forms.Form):
    cnes = forms.CharField(
        label="Número de CNES",
        max_length=20,
        help_text="Digite o número de CNES da unidade da qual você é o notificador.",
        validators=[existing_cnes_validator],
    )

    @cached_property
    def unit(self):
        cnes = self.cleaned_data["cnes"]
        return models.HealthcareUnit.objects.get(cnes_id=cnes)

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = self.request.user

    def clean(self):
        state = self.unit.city.state
        if state != self.user.state:
            state = self.user.state
            raise forms.ValidationError({"cnes": f"CNES deve ser do seu estado: {state}"})
        return self.cleaned_data

    def save(self, user):
        self.unit.register_notifier(user, authorize=False)


class FillCitiesForm(forms.Form):
    cities = forms.CharField(
        label="Lista de municípios do gestor regional",
        help_text="Inclua um município por linha e dê preferência a usar o código IBGE "
        "ao invés do nome de cada município.",
        required=False,
        widget=forms.Textarea,
    )
    state_manager = forms.BooleanField(label="Gestor estadual?", required=False)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.state = user.state
        self.cities = None

    def clean(self):
        cities = self.cleaned_data.get("cities").strip()
        state_manager = self.cleaned_data.get("state_manager")

        if not cities and not state_manager:
            raise forms.ValidationError("Preencha ao menos um dos campos.")
        if cities:
            self.process_cities(cities, validate=True)

        return self.cleaned_data

    def process_cities(self, data, validate=False):
        if self.cities is not None:
            return self.cities

        state = self.state
        data = re.split(r",\s*|\s*\n\s*", data)
        pks = {int(x) for x in data if x and x.isdigit()}
        names = {x.title() for x in data if x and not x.isdigit()}
        qs_pk = City.objects.filter(state=state, id__in=pks)
        qs_name = City.objects.filter(state=state, name__in=names)
        self.cities = (qs_pk | qs_name).distinct()

        if validate:
            expected = {*map(attrgetter("id"), self.cities), *map(attrgetter("name"), self.cities)}
            invalid = {*map(str.title, data)} - expected
            if invalid:
                invalid = ", ".join(list(invalid)[:3])
                raise forms.ValidationError({"cities": f"Cidades inválidas: {invalid}"})

        return self.cities

    def save(self):
        user = self.user

        if self.cleaned_data.get("state_manager"):
            cities = City.objects.filter(state=user.state)
        else:
            data = self.cleaned_data["cities"]
            cities = self.process_cities(data)

        associate_manager_city(user, cities)
        user.role = user.ROLE_MANAGER
        user.save()


class NotifierPendingApprovalForm(forms.ModelForm):
    class Meta:
        model = models.NotifierForHealthcareUnit
        fields = ("notifier", "unit", "is_approved")

    def __init__(self, manager=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if manager is not None:
            self.fields["notifier"].queryset = get_user_model().objects.filter(
                state_id=manager.state_id, role=get_user_model().ROLE_NOTIFIER
            )
            self.fields["unit"].queryset = models.HealthcareUnit.objects.filter(
                city__state_id=manager.state_id
            )

    def save(self, commit=True):
        obj = super().save(commit)
        if obj.is_approved and not obj.notifier.is_authorized:
            obj.notifier.is_authorized = True
            obj.notifier.save()
        return obj
