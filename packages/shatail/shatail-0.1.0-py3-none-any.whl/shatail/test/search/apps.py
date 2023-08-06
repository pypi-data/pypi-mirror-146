from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSearchTestsAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "shatail.test.search"
    label = "searchtests"
    verbose_name = _("Shatail search tests")
