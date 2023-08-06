from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailStyleGuideAppConfig(AppConfig):
    name = "shatail.contrib.styleguide"
    label = "shatailstyleguide"
    verbose_name = _("Shatail style guide")
