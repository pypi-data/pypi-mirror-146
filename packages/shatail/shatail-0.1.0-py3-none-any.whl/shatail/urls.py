from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from shatail import views
from shatail.coreutils import SHATAIL_APPEND_SLASH

if SHATAIL_APPEND_SLASH:
    # If SHATAIL_APPEND_SLASH is True (the default value), we match a
    # (possibly empty) list of path segments ending in slashes.
    # CommonMiddleware will redirect requests without a trailing slash to
    # a URL with a trailing slash
    serve_pattern = r"^((?:[\w\-]+/)*)$"
else:
    # If SHATAIL_APPEND_SLASH is False, allow Shatail to serve pages on URLs
    # with and without trailing slashes
    serve_pattern = r"^([\w\-/]*)$"


SHATAIL_FRONTEND_LOGIN_TEMPLATE = getattr(
    settings, "SHATAIL_FRONTEND_LOGIN_TEMPLATE", "shatailcore/login.html"
)


urlpatterns = [
    path(
        "_util/authenticate_with_password/<int:page_view_restriction_id>/<int:page_id>/",
        views.authenticate_with_password,
        name="shatailcore_authenticate_with_password",
    ),
    path(
        "_util/login/",
        auth_views.LoginView.as_view(template_name=SHATAIL_FRONTEND_LOGIN_TEMPLATE),
        name="shatailcore_login",
    ),
    # Front-end page views are handled through Shatail's core.views.serve
    # mechanism
    re_path(serve_pattern, views.serve, name="shatail_serve"),
]
