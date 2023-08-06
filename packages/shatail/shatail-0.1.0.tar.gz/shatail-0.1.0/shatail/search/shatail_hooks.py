from django.urls import include, path

from shatail import hooks
from shatail.search.urls import admin as admin_urls


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("search/", include(admin_urls, namespace="shatailsearch_admin")),
    ]
