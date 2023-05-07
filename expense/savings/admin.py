from django.contrib import admin

from .forms import SavingActionAdminForm
from .models import Saving, SavingAction


@admin.register(SavingAction)
class SavingActionAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "amount",
        "action",
        "date",
        "created_at",
        "belongs_to",
    ]
    form = SavingActionAdminForm


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    list_display = ["amount", "belongs_to"]
