# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shatailredirects", "0002_add_verbose_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="redirect",
            name="site",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                null=True,
                to="shatailcore.Site",
                verbose_name="Site",
                blank=True,
                related_name="redirects",
            ),
        ),
    ]
