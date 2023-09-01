import decimal
from typing import TypedDict


class AccountBalance(TypedDict):
    name: str
    balance: decimal.Decimal
    url: str
    slug: str
