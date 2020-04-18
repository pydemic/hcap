from django import forms

from hcap_geo.models import Region

from django_select2.forms import ModelSelect2MultipleWidget


class FillCitiesForm(forms.Form):
    cities = forms.ModelMultipleChoiceField(
        widget=ModelSelect2MultipleWidget(
            queryset=Region.objects.none(),
            search_fields=["name__icontains"],
            attrs={
                "data-placeholder": "Digite o nome de uma cidade.",
                "data-minimum-input-length": 2,
            },
        ),
        queryset=Region.objects.filter(kind=Region.KIND_CITY),
        required=False,
    )
    state_manager = forms.BooleanField(label="Gestor estadual?", required=False)

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["cities"].widget.queryset = Region.objects.filter(kind=Region.KIND_CITY)
        self.fields["cities"].queryset = Region.objects.filter(kind=Region.KIND_CITY)

    def clean(self):
        cities = self.cleaned_data.get("cities")
        state_manager = self.cleaned_data.get("state_manager")

        if not cities and not state_manager:
            raise forms.ValidationError("Preencha ao menos um dos campos.")

        return self.cleaned_data

    def save(self):
        user = self.user

        if self.cleaned_data.get("state_manager"):
            cities = Region.objects.filter(kind=Region.KIND_CITY)
        else:
            cities = self.cleaned_data["cities"]

        associate_manager_city(user, cities)
        user.role = user.ROLE_MANAGER
        user.save()
