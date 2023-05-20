# Generated by Django 4.2.1 on 2023-05-20 00:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_accountaction_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounttype",
            name="type",
            field=models.TextField(
                choices=[
                    ("INCOME", "Income"),
                    ("SAVING", "Saving"),
                    ("CASH", "Cash"),
                    ("OTHER", "Other"),
                ],
                default="OTHER",
                max_length=255,
            ),
        ),
    ]
