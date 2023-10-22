from django.contrib.humanize.templatetags.humanize import intcomma
from rest_framework import serializers


class MoneyField(serializers.DecimalField):
    def to_representation(self, value):
        val = super().to_representation(value)
        return intcomma(val)


class AccountBalanceSerializer(serializers.Serializer):
    name = serializers.CharField()
    balance = MoneyField(decimal_places=2, max_digits=12)
    url = serializers.CharField()
    slug = serializers.SlugField()
