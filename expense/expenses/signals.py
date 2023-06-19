def create_expense_category_for_newly_created_user(sender, instance, created, **kwargs):
    if created:
        from django.utils.text import slugify

        from .models import Category

        categories = []
        for name in [
            "Food",
            "Grocery",
            "Transport",
            "Fuel",
            "Entertainment",
            "Health",
        ]:
            categories.append(
                Category(name=name, belongs_to=instance, slug=slugify(name))
            )

        Category.objects.bulk_create(categories)
