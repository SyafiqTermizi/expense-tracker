from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import get_random_string

from expense.expenses.models import Image as ExpenseImage


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Returns an overview of the user's account balance and spending activities
    """

    # 1. Get account balance
    accounts = []
    for balance in (
        request.user.account_balances.order_by(
            "action__account__name",
            "-created_at",
        )
        .select_related("action__account")
        .distinct("action__account__name")
    ):
        accounts.append(
            {
                "name": balance.action.account.name,
                "balance": balance.amount,
                "url": balance.action.account.get_absolute_url(),
            }
        )

    # 1.1 Add accounts with no balance
    for account in request.user.accounts.exclude(
        name__in=list(map(lambda acc: acc["name"], accounts))
    ):
        accounts.append(
            {
                "name": account.name,
                "balance": 0,
                "url": account.get_absolute_url(),
            }
        )

    # 2. Get account activities for current month
    account_actions = (
        request.user.account_actions.filter(
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        )
        .order_by("-created_at")
        .select_related("expense", "account")
        .prefetch_related("expense__images")
    )

    expense_image_mapping = {}
    for image in ExpenseImage.objects.filter(
        expense__belongs_to=request.user
    ).select_related("expense"):
        expense_image_mapping.update({image.expense.pk: image.image.url})

    activities = []
    for action in account_actions:
        data = {
            "account": str(action.account),
            "created_at": action.created_at.strftime("%d/%m/%Y"),
            "description": action.description,
            "amount": action.amount,
            "action": action.action,
        }

        if hasattr(action, "expense"):
            data.update(
                {
                    "expense": True,
                    "image": expense_image_mapping.get(action.expense.pk),
                    "uid": get_random_string(10),
                }
            )

        activities.append(data)

    # 3. Get expenses for current month
    expenses = list(
        map(
            lambda expense: {
                "category": expense["category__name"],
                "amount": expense["amount"],
            },
            request.user.expenses.filter(
                created_at__month=timezone.now().month,
                created_at__year=timezone.now().year,
            )
            .values("category__name")
            .annotate(amount=Sum("amount")),
        )
    )

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "accounts": accounts,
            "activities": activities,
            "expenses": expenses,
        },
    )
