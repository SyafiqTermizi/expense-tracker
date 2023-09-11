import pytest

from expense.accounts.tests.factories import (
    AccountActionFactory,
    AccountBalanceFactory,
    AccountFactory,
    UserFactory,
)


@pytest.fixture
def user_data():
    user = UserFactory.create()
    user.set_password("abc123")
    user.save()
    user.refresh_from_db()

    account = AccountFactory.create(belongs_to=user)
    action = AccountActionFactory.create(
        account=account,
        action="CREDIT",
        belongs_to=user,
    )

    AccountBalanceFactory.create(action=action, belongs_to=user, amount=1000)

    return {
        "user": user,
        "account": account,
        "expense_categories": user.expense_categories.first(),
    }


@pytest.fixture
def authenticated_client(client, user_data):
    client.login(username=user_data["user"].email, password="abc123")
    return client
