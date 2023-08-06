# -*- coding: utf-8 -*-
from django.db import migrations


def initial_data(apps, schema_editor):
    Collection = apps.get_model("shatailcore.Collection")

    # Create root page
    Collection.objects.create(
        name="Root",
        path="0001",
        depth=1,
        numchild=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("shatailcore", "0024_collection"),
    ]

    operations = [
        migrations.RunPython(initial_data, migrations.RunPython.noop),
    ]
