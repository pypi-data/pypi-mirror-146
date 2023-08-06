from django.urls import path

from shatail.users.views import users

app_name = "shatailusers_users"
urlpatterns = [
    path("", users.index, name="index"),
    path("add/", users.create, name="add"),
    path("<str:user_id>/", users.edit, name="edit"),
    path("<str:user_id>/delete/", users.delete, name="delete"),
]
