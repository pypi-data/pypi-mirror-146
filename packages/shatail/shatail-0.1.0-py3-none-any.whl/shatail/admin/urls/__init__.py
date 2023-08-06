import functools
import hashlib

from django.conf import settings
from django.http import Http404
from django.urls import include, path, re_path
from django.views.decorators.cache import never_cache
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from shatail import hooks
from shatail.admin.api import urls as api_urls
from shatail.admin.auth import require_admin_access
from shatail.admin.urls import collections as shatailadmin_collections_urls
from shatail.admin.urls import pages as shatailadmin_pages_urls
from shatail.admin.urls import password_reset as shatailadmin_password_reset_urls
from shatail.admin.urls import reports as shatailadmin_reports_urls
from shatail.admin.urls import workflows as shatailadmin_workflows_urls
from shatail.admin.views import account, chooser, home, tags, userbar
from shatail.admin.views.bulk_action import index as bulk_actions
from shatail.admin.views.pages import listing
from shatail.utils.urlpatterns import decorate_urlpatterns

urlpatterns = [
    path("", home.home, name="shatailadmin_home"),
    path("test404/", TemplateView.as_view(template_name="shatailadmin/404.html")),
    path("api/", include(api_urls)),
    path("failwhale/", home.error_test, name="shatailadmin_error_test"),
    # TODO: Move into shatailadmin_pages namespace
    path("pages/", listing.index, name="shatailadmin_explore_root"),
    path("pages/<int:parent_page_id>/", listing.index, name="shatailadmin_explore"),
    # bulk actions
    path(
        "bulk/<str:app_label>/<str:model_name>/<str:action>/",
        bulk_actions,
        name="shatail_bulk_action",
    ),
    path("pages/", include(shatailadmin_pages_urls, namespace="shatailadmin_pages")),
    # TODO: Move into shatailadmin_pages namespace
    path("choose-page/", chooser.browse, name="shatailadmin_choose_page"),
    path(
        "choose-page/<int:parent_page_id>/",
        chooser.browse,
        name="shatailadmin_choose_page_child",
    ),
    path("choose-page/search/", chooser.search, name="shatailadmin_choose_page_search"),
    path(
        "choose-external-link/",
        chooser.external_link,
        name="shatailadmin_choose_page_external_link",
    ),
    path(
        "choose-email-link/",
        chooser.email_link,
        name="shatailadmin_choose_page_email_link",
    ),
    path(
        "choose-phone-link/",
        chooser.phone_link,
        name="shatailadmin_choose_page_phone_link",
    ),
    path(
        "choose-anchor-link/",
        chooser.anchor_link,
        name="shatailadmin_choose_page_anchor_link",
    ),
    path("tag-autocomplete/", tags.autocomplete, name="shatailadmin_tag_autocomplete"),
    path(
        "tag-autocomplete/<slug:app_name>/<slug:model_name>/",
        tags.autocomplete,
        name="shatailadmin_tag_model_autocomplete",
    ),
    path(
        "collections/",
        include(shatailadmin_collections_urls, namespace="shatailadmin_collections"),
    ),
    path(
        "workflows/",
        include(shatailadmin_workflows_urls, namespace="shatailadmin_workflows"),
    ),
    path(
        "reports/", include(shatailadmin_reports_urls, namespace="shatailadmin_reports")
    ),
    path("account/", account.account, name="shatailadmin_account"),
    path("logout/", account.LogoutView.as_view(), name="shatailadmin_logout"),
    path(
        "jsi18n/",
        JavaScriptCatalog.as_view(packages=["shatail.admin"]),
        name="shatailadmin_javascript_catalog",
    ),
]


# Import additional urlpatterns from any apps that define a register_admin_urls hook
for fn in hooks.get_hooks("register_admin_urls"):
    urls = fn()
    if urls:
        urlpatterns += urls


# Add "shatailadmin.access_admin" permission check
urlpatterns = decorate_urlpatterns(urlpatterns, require_admin_access)

sprite_hash = None


def get_sprite_hash():
    global sprite_hash
    if not sprite_hash:
        content = str(home.sprite(None).content, "utf-8")
        sprite_hash = hashlib.sha1(
            (content + settings.SECRET_KEY).encode("utf-8")
        ).hexdigest()[:8]
    return sprite_hash


# These url patterns do not require an authenticated admin user
urlpatterns += [
    path(f"sprite-{get_sprite_hash()}/", home.sprite, name="shatailadmin_sprite"),
    path("login/", account.LoginView.as_view(), name="shatailadmin_login"),
    # These two URLs have the "permission_required" decorator applied directly
    # as they need to fail with a 403 error rather than redirect to the login page
    path(
        "userbar/<int:page_id>/",
        userbar.for_frontend,
        name="shatailadmin_userbar_frontend",
    ),
    path(
        "userbar/moderation/<int:revision_id>/",
        userbar.for_moderation,
        name="shatailadmin_userbar_moderation",
    ),
    # Password reset
    path("password_reset/", include(shatailadmin_password_reset_urls)),
]


# Default view (will show 404 page)
# This must be the last URL in this file!

if settings.APPEND_SLASH:
    # Only catch unrecognized patterns with a trailing slash
    # and let CommonMiddleware handle adding a slash to every other pattern
    urlpatterns += [
        re_path(r"^.*/$", home.default),
    ]

else:
    # Catch all unrecognized patterns
    urlpatterns += [
        re_path(r"^", home.default),
    ]


# Hook in our own 404 handler
def display_custom_404(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Http404:
            return page_not_found(request, "", template_name="shatailadmin/404.html")

    return wrapper


urlpatterns = decorate_urlpatterns(urlpatterns, display_custom_404)


# Decorate all views with cache settings to prevent caching
urlpatterns = decorate_urlpatterns(urlpatterns, never_cache)
