from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailAppConfig(AppConfig):
    name = "shatail"
    label = "shatailcore"
    verbose_name = _("Shatail core")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from shatail.signal_handlers import register_signal_handlers

        register_signal_handlers()

        from shatail import widget_adapters  # noqa
