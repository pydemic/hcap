from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm


class ResetPasswordForm(AllauthResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"].widget.attrs["placeholder"]
