import django_filters
from django.utils.translation import gettext as _

from shatail.admin.filters import ShatailFilterSet
from shatail.admin.widgets import ButtonSelect
from shatail.models import Site


class RedirectsReportFilterSet(ShatailFilterSet):
    is_permanent = django_filters.ChoiceFilter(
        label=_("Type"),
        method="filter_type",
        choices=(
            (True, _("Permanent")),
            (False, _("Temporary")),
        ),
        empty_label=_("All"),
        widget=ButtonSelect,
    )

    site = django_filters.ModelChoiceFilter(
        field_name="site", queryset=Site.objects.all()
    )

    def filter_type(self, queryset, name, value):
        if value and self.request and self.request.user:
            queryset = queryset.filter(is_permanent=value)
        return queryset
