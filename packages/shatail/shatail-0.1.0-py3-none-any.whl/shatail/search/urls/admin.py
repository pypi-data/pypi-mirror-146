from django.urls import path

from shatail.search.views import queries

app_name = "shatailsearch_admin"
urlpatterns = [
    path("queries/chooser/", queries.chooser, name="queries_chooser"),
    path(
        "queries/chooser/results/",
        queries.chooserresults,
        name="queries_chooserresults",
    ),
]
