from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data

        user.cpf = data.get("cpf")
        user.email = data.get("email")
        user.name = data.get("name")

        user.set_password(data.get("password1"))

        user.full_clean()

        if commit:
            user.save()

        return user
