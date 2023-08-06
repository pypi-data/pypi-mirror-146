from django.urls import path

from shatail import hooks
from shatail.api.v2.router import ShatailAPIRouter

from .views import PagesAdminAPIViewSet

admin_api = ShatailAPIRouter("shatailadmin_api")
admin_api.register_endpoint("pages", PagesAdminAPIViewSet)

for fn in hooks.get_hooks("construct_admin_api"):
    fn(admin_api)

urlpatterns = [
    path("main/", admin_api.urls),
]
