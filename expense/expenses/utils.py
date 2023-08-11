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
                "category": expense["category__name"],
                "id": expense["pk"],
                "expense": True,
            },
            user_monthly_expenses,
        )
    )
