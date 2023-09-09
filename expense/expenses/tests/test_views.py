from django.urls import reverse

from expense.accounts.models import Account
from expense.accounts.tests.factories import (
    AccountActionFactory,
    AccountBalanceFactory,
    AccountFactory,
    UserFactory,
)


def test_add_expense_view_unauthenticated_user(db, client):
    """
    Accessing expense add view with an unauthenticated user will return 302
    """
    user = UserFactory.create(password="abc123")
    account = AccountFactory.create(belongs_to=user)
    action = AccountActionFactory.create(
        account=account,
        action="CREDIT",
        belongs_to=user,
    )
    AccountBalanceFactory.create(action=action, belongs_to=user)

    # client.login(username=user.username, password=user.password)
    res = client.get(reverse("expenses:add"))

    assert res.status_code == 302
