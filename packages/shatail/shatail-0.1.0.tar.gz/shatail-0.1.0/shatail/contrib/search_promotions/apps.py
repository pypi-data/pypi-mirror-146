from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailSearchPromotionsAppConfig(AppConfig):
    name = "shatail.contrib.search_promotions"
    label = "shatailsearchpromotions"
    verbose_name = _("Shatail search promotions")
    default_auto_field = "django.db.models.AutoField"
