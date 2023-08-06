# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shatailredirects", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="redirect",
            options={"verbose_name": "Redirect"},
        ),
        migrations.AlterField(
            model_name="redirect",
            name="site",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="redirects",
                blank=True,
                editable=False,
                to="shatailcore.Site",
                null=True,
                verbose_name="Site",
            ),
        ),
    ]
