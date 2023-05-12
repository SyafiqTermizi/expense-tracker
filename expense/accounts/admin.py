from django.contrib import admin

from .forms import AccountActionAdminForm
from .models import Account, AccountAction


@admin.register(AccountAction)
class AccountAction(admin.ModelAdmin):
    list_display = [
        "description",
        "amount",
        "action",
        "date",
        "created_at",
        "belongs_to",
    ]
    form = AccountActionAdminForm


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["amount", "belongs_to"]
