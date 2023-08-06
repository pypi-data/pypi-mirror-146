from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailModelAdminAppConfig(AppConfig):
    name = "shatail.contrib.modeladmin"
    label = "shatailmodeladmin"
    verbose_name = _("Shatail ModelAdmin")
