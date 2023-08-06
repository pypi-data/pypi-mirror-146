from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import checks  # NOQA


class ShatailAdminAppConfig(AppConfig):
    name = "shatail.admin"
    label = "shatailadmin"
    verbose_name = _("Shatail admin")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from shatail.admin.signal_handlers import register_signal_handlers

        register_signal_handlers()
