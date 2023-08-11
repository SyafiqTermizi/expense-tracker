from django.contrib import admin

from .forms import AccountActionForm
from .models import AccountAction, AccountBalance


@admin.register(AccountAction)
class AccountAction(admin.ModelAdmin):
    list_display = [
        "description",
        "amount",
        "action",
        "created_at",
        "created_at",
        "belongs_to",
    ]
    form = AccountActionForm


@admin.register(AccountBalance)
class AccountBalanceAdmin(admin.ModelAdmin):
    list_display = ["amount", "belongs_to", "account"]
