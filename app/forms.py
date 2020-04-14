import re
from operator import attrgetter

from django import forms
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.functional import cached_property

from locations.models import City, associate_manager_city
from . import models
from .validators import existing_cnes_validator

from django_select2.forms import ModelSelect2MultipleWidget


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
    cities = forms.ModelMultipleChoiceField(
        widget=ModelSelect2MultipleWidget(
            queryset=City.objects.none(),
            search_fields=["name__icontains"],
            attrs={
                "data-placeholder": "Digite o nome de uma cidade.",
                "data-minimum-input-length": 2,
            },
        ),
        queryset=City.objects.all(),
        required=False,
    )
    state_manager = forms.BooleanField(label="Gestor estadual?", required=False)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.state = user.state
        self.fields["cities"].widget.queryset = City.objects.filter(state=self.user.state)
        self.fields["cities"].queryset = City.objects.filter(state=self.user.state)

    def clean(self):
        cities = self.cleaned_data.get("cities")
        state_manager = self.cleaned_data.get("state_manager")

        if not cities and not state_manager:
            raise forms.ValidationError("Preencha ao menos um dos campos.")

        return self.cleaned_data

    def save(self):
        user = self.user

        if self.cleaned_data.get("state_manager"):
            cities = City.objects.filter(state=user.state)
        else:
            cities = self.cleaned_data["cities"]

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
