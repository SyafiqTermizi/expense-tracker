# Generated by Django 4.2.4 on 2023-09-01 02:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_accountbalance_belongs_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountaction",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name="accountbalance",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
