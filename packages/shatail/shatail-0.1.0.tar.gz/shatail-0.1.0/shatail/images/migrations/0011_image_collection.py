# -*- coding: utf-8 -*-
from django.db import migrations, models

import shatail.models


class Migration(migrations.Migration):

    dependencies = [
        ("shatailcore", "0026_group_collection_permission"),
        ("shatailimages", "0010_change_on_delete_behaviour"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="collection",
            field=models.ForeignKey(
                to="shatailcore.Collection",
                verbose_name="collection",
                default=shatail.models.get_root_collection_id,
                related_name="+",
                on_delete=models.CASCADE,
            ),
        ),
    ]
