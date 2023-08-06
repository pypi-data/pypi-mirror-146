# -*- coding: utf-8 -*-
from django.db import migrations


def add_page_lock_permission_to_moderators(apps, schema_editor):
    Group = apps.get_model("auth.Group")
    Page = apps.get_model("shatailcore.Page")
    GroupPagePermission = apps.get_model("shatailcore.GroupPagePermission")

    root_pages = Page.objects.filter(depth=1)

    try:
        moderators_group = Group.objects.get(name="Moderators")

        for page in root_pages:
            GroupPagePermission.objects.create(
                group=moderators_group, page=page, permission_type="lock"
            )

    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("shatailcore", "0004_page_locked"),
    ]

    operations = [
        migrations.RunPython(add_page_lock_permission_to_moderators),
    ]
