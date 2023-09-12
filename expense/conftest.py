import pytest

from expense.accounts.tests.factories import (
    AccountActionFactory,
    AccountBalanceFactory,
    AccountFactory,
    UserFactory,
)
from expense.expenses.forms import AddExpenseForm


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


@pytest.fixture
def create_user_expense(user_data):
    def inner(with_image=False):
        data = {
            "amount": 1,
            "description": "test",
            "category": user_data["expense_categories"].slug,
            "from_account": user_data["account"].slug,
        }

        if with_image:
            with open("expense/expenses/tests/testfiles/validpng.png", "rb") as image:
                data.update({"image": image})

        form = AddExpenseForm(
            user=user_data["user"],
            data=data,
        )

        assert form.is_valid()
        return form.save()

    return inner
