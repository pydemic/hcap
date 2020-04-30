from django import forms

from hcap_accounts.models import RegionManager


class PendingManagerAuthorizationForm(forms.ModelForm):
    class Meta:
        model = RegionManager
        fields = ("region", "user", "is_authorized")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].disabled = True
        self.fields["user"].disabled = True
