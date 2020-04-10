from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.email = data.get("email")
        user.cpf = data.get("cpf")
        user.state = data.get("state")
        user.set_password(data.get("password1"))
        if commit:
            user.save()
        return user
