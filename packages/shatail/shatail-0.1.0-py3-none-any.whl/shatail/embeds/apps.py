from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .finders import get_finders


class ShatailEmbedsAppConfig(AppConfig):
    name = "shatail.embeds"
    label = "shatailembeds"
    verbose_name = _("Shatail embeds")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        # Check configuration on startup
        get_finders()
