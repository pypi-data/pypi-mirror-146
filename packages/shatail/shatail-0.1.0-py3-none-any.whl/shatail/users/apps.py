from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShatailUsersAppConfig(AppConfig):
    name = "shatail.users"
    label = "shatailusers"
    verbose_name = _("Shatail users")
    default_auto_field = "django.db.models.AutoField"
    group_viewset = "shatail.users.views.groups.GroupViewSet"
