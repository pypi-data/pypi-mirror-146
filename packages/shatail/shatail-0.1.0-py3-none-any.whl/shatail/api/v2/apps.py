from django.apps import AppConfig, apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _


class ShatailAPIV2AppConfig(AppConfig):
    name = "shatail.api.v2"
    label = "shatailapi_v2"
    verbose_name = _("Shatail API v2")

    def ready(self):
        # Install cache purging signal handlers
        if getattr(settings, "SHATAILAPI_USE_FRONTENDCACHE", False):
            if apps.is_installed("shatail.contrib.frontend_cache"):
                from shatail.api.v2.signal_handlers import register_signal_handlers

                register_signal_handlers()
            else:
                raise ImproperlyConfigured(
                    "The setting 'SHATAILAPI_USE_FRONTENDCACHE' is True but 'shatail.contrib.frontend_cache' is not in INSTALLED_APPS."
                )
