from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

AnonymousUser.cpf = "000.000.000-00"
AnonymousUser.has_verified_email = False
AnonymousUser.is_authorized = False
AnonymousUser.is_manager = False
AnonymousUser.is_notifier = False
AnonymousUser.name = _("Guest")
