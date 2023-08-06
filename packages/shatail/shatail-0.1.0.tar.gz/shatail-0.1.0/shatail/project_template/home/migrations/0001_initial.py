# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shatailcore", "0040_page_draft_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        parent_link=True,
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        to="shatailcore.Page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("shatailcore.page",),
        ),
    ]
