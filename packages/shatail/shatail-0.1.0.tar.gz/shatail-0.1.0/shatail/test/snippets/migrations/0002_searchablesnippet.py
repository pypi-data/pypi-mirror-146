# -*- coding: utf-8 -*-
from django.db import migrations, models

import shatail.search.index


class Migration(migrations.Migration):

    dependencies = [
        ("snippetstests", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SearchableSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
            ],
            bases=(shatail.search.index.Indexed, models.Model),
        ),
    ]
