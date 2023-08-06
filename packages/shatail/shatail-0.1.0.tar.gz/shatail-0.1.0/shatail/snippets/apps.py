from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSnippetsAppConfig(AppConfig):
    name = "shatail.snippets"
    label = "shatailsnippets"
    verbose_name = _("Shatail snippets")
