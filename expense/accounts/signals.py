def create_account_for_newly_created_user(sender, instance, created, **kwargs):
    if created:
        from .models import AccountType

        account_types = []
        for account_type in ["INCOME", "SAVING", "CASH"]:
            account_types.append(
                AccountType(
                    type=account_type,
                    description=f"{account_type.title()} account",
                    belongs_to=instance,
                )
            )

        AccountType.objects.bulk_create(account_types)
