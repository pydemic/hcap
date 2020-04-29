from django import forms
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from hcap_accounts.models import RegionManager
from hcap_geo.models import Region


class ManagerCitiesAuthorizationRequestForm(forms.Form):
    state = forms.ModelChoiceField(
        Region.objects.filter(kind=Region.KIND_STATE),
        label=_("State"),
        empty_label=None,
        disabled=True,
        required=False,
    )

    state_hidden = forms.CharField(widget=forms.HiddenInput())

    cities = forms.ModelMultipleChoiceField(
        Region.objects.none(), label=_("Cities"), widget=forms.CheckboxSelectMultiple
    )

    managers = []

    def __init__(self, *args, user, state_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["state"].queryset = Region.objects.filter(id=state_id)
        self.fields["state_hidden"].initial = state_id
        self.fields["cities"].queryset = Region.objects.filter(
            kind=Region.KIND_CITY, parents__id=state_id
        )

    def clean(self):
        cleaned_data = super().clean()

        managers = []
        invalid_cities = []

        for city in cleaned_data["cities"]:
            try:
                manager = RegionManager(user=self.user, region=city, is_authorized=False)
                manager.full_clean()
                managers.append(manager)
            except DjangoValidationError as exception:
                error = exception.error_dict.get("__all__", [None])[0]
                if error is not None and error.code == "unique_together":
                    invalid_cities.append(city.name)
                else:
                    raise exception

        length = len(invalid_cities)
        if length != 0:
            message = ngettext_lazy(
                "You already have authorization request for the following city: %(cities)s.",
                "You already have authorization request for the following cities: %(cities)s.",
                length,
            )
            self.add_error("cities", message % {"cities": ", ".join(invalid_cities)})

        self.managers = managers

        return cleaned_data

    def save(self):
        if len(self.managers) != 0:
            RegionManager.objects.bulk_create(self.managers)
