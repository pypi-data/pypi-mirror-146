# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shatailembeds", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="embed",
            options={"verbose_name": "Embed"},
        ),
    ]
