from django.conf import settings
from django.utils.crypto import get_random_string


def get_formatted_user_expense_for_month(user_monthly_expenses: list) -> list:
    """
    To be used with ExpenseMananger.get_user_expense_for_month
    """
    return list(
        map(
            lambda expense: {
                "account": expense["from_action__account__name"],
                "created_at": expense["created_at"],
                "description": expense["description"],
                "amount": expense["amount"],
                "image": f"{settings.MEDIA_URL}{expense['images__image']}"
                if expense["images__image"]
                else None,
                "category": expense["category__name"],
                "uid": get_random_string(10),
            },
            user_monthly_expenses,
        )
    )
