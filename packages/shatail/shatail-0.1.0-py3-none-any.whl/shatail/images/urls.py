from django.urls import re_path

from shatail.images.views.serve import serve

urlpatterns = [
    re_path(r"^([^/]*)/(\d*)/([^/]*)/[^/]*$", serve, name="shatailimages_serve"),
]
