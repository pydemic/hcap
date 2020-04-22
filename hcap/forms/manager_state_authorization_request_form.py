from django import forms
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hcap_accounts.models import RegionManager
from hcap_geo.models import Region


class ManagerStateAuthorizationRequestForm(forms.Form):
    state = forms.ModelChoiceField(
        Region.objects.filter(kind=Region.KIND_STATE), label=_("State"), initial=0
    )

    request_for_state = forms.BooleanField(
        label=_("Request to manage state?"),
        required=False,
        help_text=_(
            "If not checked, the form will update with a list of cities from the selected state."
        ),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self):
        if self.cleaned_data["request_for_state"] is True:
            try:
                manager = RegionManager(
                    user=self.user, region=self.cleaned_data["state"], is_authorized=False
                )
                manager.full_clean()
                manager.save()
            except DjangoValidationError as exception:
                error = exception.error_dict.get("__all__", [None])[0]
                if error is None or error.code != "unique_together":
                    raise exception

    def is_cities_request(self):
        return not self.cleaned_data["request_for_state"]

    def get_state(self):
        return self.cleaned_data["state"]
