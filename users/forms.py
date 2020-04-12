from allauth.account.forms import (
    ChangePasswordForm as AllauthChangePasswordForm,
    LoginForm as AllauthLoginForm,
    ResetPasswordForm as AllauthResetPasswordForm,
    SignupForm as AllauthSignupForm,
)
from users.validators import CPFValidator
from material import Layout, Row
from django import forms
from django.contrib.auth import get_user_model
from locations.models import State


class ChangePasswordForm(AllauthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["oldpassword"].widget.attrs["placeholder"]
        del self.fields["password1"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["login"].widget.attrs["placeholder"]
        del self.fields["password"].widget.attrs["placeholder"]


class ResetPasswordForm(AllauthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"].widget.attrs["placeholder"]


class SignupForm(AllauthSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password1"].widget.attrs["placeholder"]
        del self.fields["email"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]

    cpf = forms.CharField(
        label="CPF",
        min_length=14,
        max_length=14,
        widget=forms.TextInput(attrs={"data-mask": "000.000.000-00"}),
        validators=[CPFValidator()],
    )

    name = forms.CharField(
        label="Nome completo", min_length=3, max_length=100, widget=forms.TextInput()
    )

    state = forms.ModelChoiceField(
        label="Estado", queryset=State.objects.all(), empty_label="Escolha um estado"
    )

    layout = Layout("name", "cpf", "email", "state", "password1", "password2")

    def clean(self):
        super().clean()

        if get_user_model().objects.filter(cpf=self.cleaned_data.get("cpf")).exists():
            self.add_error("cpf", "Este CPF já foi registrado.")

        return self.cleaned_data
