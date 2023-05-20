def create_account_for_newly_created_user(sender, instance, created, **kwargs):
    if created:
        from .models import AccountType

        for account_type in ["INCOME", "SAVING", "CASH"]:
            AccountType.objects.create(
                type=account_type,
                description=f"{account_type.title()} account",
                belongs_to=instance,
            )
