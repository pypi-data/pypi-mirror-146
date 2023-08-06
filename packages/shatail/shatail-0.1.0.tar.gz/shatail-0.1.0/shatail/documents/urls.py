from django.urls import path, re_path

from shatail.documents.views import serve

urlpatterns = [
    re_path(r"^(\d+)/(.*)$", serve.serve, name="shataildocs_serve"),
    path(
        "authenticate_with_password/<int:restriction_id>/",
        serve.authenticate_with_password,
        name="shataildocs_authenticate_with_password",
    ),
]
