from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailFormsAppConfig(AppConfig):
    name = "shatail.contrib.forms"
    label = "shatailforms"
    verbose_name = _("Shatail forms")
    default_auto_field = "django.db.models.AutoField"
