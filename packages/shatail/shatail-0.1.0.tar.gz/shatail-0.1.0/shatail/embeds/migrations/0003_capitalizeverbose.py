# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shatailembeds", "0002_add_verbose_names"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="embed",
            options={"verbose_name": "embed"},
        ),
    ]
