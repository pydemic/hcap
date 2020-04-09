from allauth.account.forms import SignupForm as AllauthSignupForm
from users.validators import CPFValidator
from django import forms
from django.contrib.auth import get_user_model
from locations.models import State


class SignupForm(AllauthSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["email"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]

    cpf = forms.CharField(
        label="CPF",
        min_length=14,
        max_length=14,
        widget=forms.TextInput(attrs={"data-mask": "000.000.000-00"}),
        validators=[CPFValidator()],
    )

    first_name = forms.CharField(
        label="Nome", min_length=3, max_length=100, widget=forms.TextInput()
    )

    last_name = forms.CharField(
        label="Sobrenome", min_length=3, max_length=100, widget=forms.TextInput()
    )

    state = forms.ModelChoiceField(
        label="Estado", queryset=State.objects.all(), empty_label="Escolha um estado"
    )

    def clean(self):
        super().clean()

        if get_user_model().objects.filter(cpf=self.cleaned_data.get("cpf")).exists():
            self.add_error("cpf", "Este CPF já foi registrado.")

        return self.cleaned_data
