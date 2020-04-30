from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy as _

AdminSite.index_title = _("Administrative Panel")
AdminSite.site_header = _("Hospital Capacity Administration")
AdminSite.site_title = _("HCap Admin")
