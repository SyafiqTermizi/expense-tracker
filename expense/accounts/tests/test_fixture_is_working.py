from .factories import AccountBalanceFactory


def test_fixture_is_working(db):
    balance = AccountBalanceFactory()
    assert balance.amount
