# Generated by Django 4.2.2 on 2023-07-02 10:41

from django.db import migrations, models
import django.db.models.deletion
import expense.expenses.models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0002_category_slug_category_unique_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=expense.expenses.models.get_upload_path
                    ),
                ),
                (
                    "expense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="expenses.expense",
                    ),
                ),
            ],
        ),
    ]
