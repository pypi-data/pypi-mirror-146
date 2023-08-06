from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailTestsAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "shatail.test.modeladmintest"
    label = "modeladmintest"
    verbose_name = _("Test Shatail Model Admin")
