from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailRoutablePageAppConfig(AppConfig):
    name = "shatail.contrib.routable_page"
    label = "shatailroutablepage"
    verbose_name = _("Shatail routablepage")
