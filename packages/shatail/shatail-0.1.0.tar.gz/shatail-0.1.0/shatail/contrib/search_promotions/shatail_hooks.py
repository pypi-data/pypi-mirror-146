from django.contrib.auth.models import Permission
from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _

from shatail import hooks
from shatail.admin.admin_url_finder import (
    ModelAdminURLFinder,
    register_admin_url_finder,
)
from shatail.admin.menu import MenuItem
from shatail.contrib.search_promotions import admin_urls
from shatail.permission_policies import ModelPermissionPolicy

from .models import SearchPromotion


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("searchpicks/", include(admin_urls, namespace="shatailsearchpromotions")),
    ]


class SearchPicksMenuItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm("shatailsearchpromotions.add_searchpromotion")
            or request.user.has_perm("shatailsearchpromotions.change_searchpromotion")
            or request.user.has_perm("shatailsearchpromotions.delete_searchpromotion")
        )


@hooks.register("register_settings_menu_item")
def register_search_picks_menu_item():
    return SearchPicksMenuItem(
        _("Promoted search results"),
        reverse("shatailsearchpromotions:index"),
        icon_name="pick",
        order=900,
    )


@hooks.register("register_permissions")
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label="shatailsearchpromotions",
        codename__in=[
            "add_searchpromotion",
            "change_searchpromotion",
            "delete_searchpromotion",
        ],
    )


class SearchPromotionAdminURLFinder(ModelAdminURLFinder):
    permission_policy = ModelPermissionPolicy(SearchPromotion)

    def construct_edit_url(self, instance):
        return reverse("shatailsearchpromotions:edit", args=(instance.query.id,))


register_admin_url_finder(SearchPromotion, SearchPromotionAdminURLFinder)
