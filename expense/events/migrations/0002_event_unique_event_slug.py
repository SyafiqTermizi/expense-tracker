# Generated by Django 4.2.5 on 2023-09-07 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="event",
            constraint=models.UniqueConstraint(
                fields=("slug", "belongs_to"), name="unique_event_slug"
            ),
        ),
    ]