# Generated by Django 4.2.4 on 2023-08-11 15:25
from django.db import migrations
from django.utils.crypto import get_random_string


def generate_random_string(apps, schema_editor):
    Expense = apps.get_model("expenses", "Expense")
    for row in Expense.objects.all():
        row.slug = get_random_string(15)
        row.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0004_expense_slug"),
    ]

    operations = [
        migrations.RunPython(
            generate_random_string,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
