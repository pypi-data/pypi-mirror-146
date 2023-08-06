from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSitemapsAppConfig(AppConfig):
    name = "shatail.contrib.sitemaps"
    label = "shatailsitemaps"
    verbose_name = _("Shatail sitemaps")
