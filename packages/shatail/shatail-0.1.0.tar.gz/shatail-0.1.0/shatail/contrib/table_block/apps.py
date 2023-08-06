from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailTableBlockAppConfig(AppConfig):
    name = "shatail.contrib.table_block"
    label = "shatailtableblock"
    verbose_name = _("Shatail table block")
