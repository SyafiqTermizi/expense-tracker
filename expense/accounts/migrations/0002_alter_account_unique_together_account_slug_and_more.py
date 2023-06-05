# Generated by Django 4.2.1 on 2023-06-05 04:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="account",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="account",
            name="slug",
            field=models.SlugField(
                default=datetime.datetime(
                    2023, 6, 5, 4, 18, 34, 361452, tzinfo=datetime.timezone.utc
                ),
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="account",
            name="description",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddConstraint(
            model_name="account",
            constraint=models.UniqueConstraint(
                fields=("name", "belongs_to"), name="unique_account"
            ),
        ),
        migrations.AddConstraint(
            model_name="account",
            constraint=models.UniqueConstraint(
                fields=("slug", "belongs_to"), name="unique_slug"
            ),
        ),
    ]