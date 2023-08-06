from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailLocalesAppConfig(AppConfig):
    name = "shatail.locales"
    label = "shataillocales"
    verbose_name = _("Shatail locales")
