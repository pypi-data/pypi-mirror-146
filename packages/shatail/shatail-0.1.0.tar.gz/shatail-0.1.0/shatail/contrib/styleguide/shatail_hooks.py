from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from shatail import hooks
from shatail.admin.menu import MenuItem

from . import views


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("styleguide/", views.index, name="shatailstyleguide"),
    ]


@hooks.register("register_settings_menu_item")
def register_styleguide_menu_item():
    return MenuItem(
        _("Styleguide"), reverse("shatailstyleguide"), icon_name="image", order=1000
    )
