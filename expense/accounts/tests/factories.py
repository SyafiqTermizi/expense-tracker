import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from expense.accounts.models import Account, AccountAction, AccountBalance
from expense.users.tests.factories import UserFactory


class AccountFactory(DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.Faker("slug")
    description = factory.Faker("text")
    belongs_to = factory.SubFactory(UserFactory)

    class Meta:
        model = Account


class AccountActionFactory(DjangoModelFactory):
    description = factory.Faker("text")
    amount = factory.Faker("random_number")
    action = fuzzy.FuzzyChoice(["CREDIT", "DEBIT"])
    account = factory.SubFactory(AccountFactory)
    belongs_to = factory.SubFactory(UserFactory)

    class Meta:
        model = AccountAction


class AccountBalanceFactory(DjangoModelFactory):
    amount = factory.Faker("random_number")
    action = factory.SubFactory(AccountActionFactory)
    belongs_to = factory.SubFactory(UserFactory)

    class Meta:
        model = AccountBalance
