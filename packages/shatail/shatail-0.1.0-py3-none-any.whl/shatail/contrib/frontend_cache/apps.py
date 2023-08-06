from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from shatail.contrib.frontend_cache.signal_handlers import register_signal_handlers


class ShatailFrontendCacheAppConfig(AppConfig):
    name = "shatail.contrib.frontend_cache"
    label = "shatailfrontendcache"
    verbose_name = _("Shatail frontend cache")

    def ready(self):
        register_signal_handlers()
