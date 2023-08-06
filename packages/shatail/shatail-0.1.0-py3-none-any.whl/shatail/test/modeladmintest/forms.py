from shatail.admin.forms.models import ShatailAdminModelForm

from .models import Publisher


class PublisherModelAdminForm(ShatailAdminModelForm):
    class Meta:
        model = Publisher
        fields = ["name"]
