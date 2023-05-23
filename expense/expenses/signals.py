def create_expense_category_for_newly_created_user(sender, instance, created, **kwargs):
    if created:
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
            categories.append(Category(name=name, belongs_to=instance))

        Category.objects.bulk_create(categories)
