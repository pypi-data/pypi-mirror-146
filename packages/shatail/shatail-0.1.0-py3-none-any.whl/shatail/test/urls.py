from django.apps import apps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path

from shatail import urls as shatail_urls
from shatail.admin import urls as shatailadmin_urls
from shatail.admin.views import home
from shatail.api.v2.router import ShatailAPIRouter
from shatail.api.v2.views import PagesAPIViewSet
from shatail.contrib.sitemaps import Sitemap
from shatail.contrib.sitemaps import views as sitemaps_views
from shatail.documents import urls as shataildocs_urls
from shatail.documents.api.v2.views import DocumentsAPIViewSet
from shatail.images import urls as shatailimages_urls
from shatail.images.api.v2.views import ImagesAPIViewSet
from shatail.images.tests import urls as shatailimages_test_urls
from shatail.test.testapp import urls as testapp_urls
from shatail.test.testapp.models import EventSitemap

api_router = ShatailAPIRouter("shatailapi_v2")
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)


urlpatterns = [
    path("admin/", include(shatailadmin_urls)),
    path("documents/", include(shataildocs_urls)),
    path("testimages/", include(shatailimages_test_urls)),
    path("images/", include(shatailimages_urls)),
    path("api/main/", api_router.urls),
    path("sitemap.xml", sitemaps_views.sitemap),
    path(
        "sitemap-index.xml",
        sitemaps_views.index,
        {
            "sitemaps": {"pages": Sitemap, "events": EventSitemap(request=None)},
            "sitemap_url_name": "sitemap",
        },
    ),
    path("sitemap-<str:section>.xml", sitemaps_views.sitemap, name="sitemap"),
    path("testapp/", include(testapp_urls)),
    path("fallback/", lambda: HttpResponse("ok"), name="fallback"),
]

if apps.is_installed("pattern_library"):
    urlpatterns += [
        path(
            "pattern-library/api/v1/sprite",
            home.sprite,
            name="pattern_library_sprite",
        ),
        path("pattern-library/", include("pattern_library.urls")),
    ]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    # For anything not caught by a more specific rule above, hand over to
    # Shatail's serving mechanism
    path("", include(shatail_urls)),
]
