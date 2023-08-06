from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSitesAppConfig(AppConfig):
    name = "shatail.sites"
    label = "shatailsites"
    verbose_name = _("Shatail sites")
