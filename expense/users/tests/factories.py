import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from expense.users.models import User, CURRENCIES

CURRENCY_CODES = [x[0] for x in CURRENCIES]


class UserFactory(DjangoModelFactory):
    name = factory.Faker("name")
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    currency = fuzzy.FuzzyChoice(CURRENCY_CODES)

    class Meta:
        model = User
