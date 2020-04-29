from allauth.account.forms import ChangePasswordForm as AllauthChangePasswordForm


class ChangePasswordForm(AllauthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["oldpassword"].widget.attrs["placeholder"]
        del self.fields["password1"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]
