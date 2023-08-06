from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSnippetsTestsAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "shatail.test.snippets"
    label = "snippetstests"
    verbose_name = _("Shatail snippets tests")
