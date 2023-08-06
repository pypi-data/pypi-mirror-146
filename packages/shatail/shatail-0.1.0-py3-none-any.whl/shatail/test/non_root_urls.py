"""An alternative urlconf module where Shatail front-end URLs
are rooted at '/site/' rather than '/'"""

from django.urls import include, path

from shatail import urls as shatail_urls
from shatail.admin import urls as shatailadmin_urls
from shatail.documents import urls as shataildocs_urls
from shatail.images import urls as shatailimages_urls

urlpatterns = [
    path("admin/", include(shatailadmin_urls)),
    path("documents/", include(shataildocs_urls)),
    path("images/", include(shatailimages_urls)),
    path("site/", include(shatail_urls)),
]
