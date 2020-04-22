from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from material import Layout

from hcap_utils.contrib.validations import CPFValidator


class SignupForm(AllauthSignupForm):
    cpf = forms.CharField(
        label=_("CPF"),
        min_length=14,
        max_length=14,
        widget=forms.TextInput(attrs={"data-mask": "000.000.000-00"}),
        validators=(CPFValidator(),),
    )

    name = forms.CharField(label=_("Name"), max_length=150, widget=forms.TextInput())

    layout = Layout("name", "cpf", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password1"].widget.attrs["placeholder"]
        del self.fields["email"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]

    def clean(self):
        super().clean()

        if get_user_model().objects.filter(cpf=self.cleaned_data.get("cpf")).exists():
            self.add_error("cpf", _("CPF already registered."))

        return self.cleaned_data
