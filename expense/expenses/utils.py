from django.utils.crypto import get_random_string

from expense.expenses.models import Image


def get_formatted_user_expense_for_month(user_monthly_expenses: list) -> list:
    """
    To be used with ExpenseMananger.get_user_expense_for_month
    """

    # Get all images pk from the list
    expense_image_mapping = {}
    for image in Image.objects.filter(
        pk__in=list(
            filter(
                bool,
                map(
                    lambda expense_data: expense_data.get("images"),
                    user_monthly_expenses,
                ),
            )
        )
    ).select_related("expense"):
        expense_image_mapping.update({image.expense.pk: image.image.url})

    return list(
        map(
            lambda expense: {
                "account": expense["from_action__account__name"],
                "created_at": expense["created_at"],
                "description": expense["description"],
                "amount": expense["amount"],
                # merge image with expense from the mapping
                "image": expense_image_mapping.get(expense["pk"]),
                "category": expense["category__name"],
                "uid": get_random_string(10),
                "expense": True,
            },
            user_monthly_expenses,
        )
    )
