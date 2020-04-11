from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from django.contrib.admin import AdminSite, site
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from material.frontend.models import Module as MaterialFrontendModule

AdminSite.index_title = "Painel Administrativo"
AdminSite.site_header = "Capacidade Hospitalar - Administração"
AdminSite.site_title = "Capacidade Hospitalar"

site.unregister(EmailAddress)
site.unregister(SocialAccount)
site.unregister(SocialApp)
site.unregister(SocialToken)
site.unregister(Group)
site.unregister(Site)
site.unregister(MaterialFrontendModule)
