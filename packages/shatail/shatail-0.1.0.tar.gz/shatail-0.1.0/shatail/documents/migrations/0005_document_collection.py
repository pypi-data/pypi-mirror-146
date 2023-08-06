# -*- coding: utf-8 -*-
from django.db import migrations, models

import shatail.models


class Migration(migrations.Migration):

    dependencies = [
        ("shatailcore", "0025_collection_initial_data"),
        ("shataildocs", "0004_capitalizeverbose"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="collection",
            field=models.ForeignKey(
                related_name="+",
                to="shatailcore.Collection",
                verbose_name="collection",
                default=shatail.models.get_root_collection_id,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
