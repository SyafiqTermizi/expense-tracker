import base64

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

    AccountBalanceFactory.create(action=action, belongs_to=user)

    return {
        "user": user,
        "account": account,
        "expense_categories": user.expense_categories.first(),
    }


@pytest.fixture
def authenticated_client(client, user_data):
    client.login(username=user_data["user"].email, password="abc123")
    return client


@pytest.fixture
def image():
    return base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAUA"
        + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
        + "9TXL0Y4OHwAAAABJRU5ErkJggg=="
    )
