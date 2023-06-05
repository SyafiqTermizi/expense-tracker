from django.utils.text import slugify


def create_account_for_newly_created_user(sender, instance, created, **kwargs):
    if created:
        from .models import Account

        accounts = []
        for account_name in ["Income", "Saving", "Cash"]:
            accounts.append(
                Account(
                    name=account_name,
                    slug=slugify(account_name),
                    description=f"{account_name} account",
                    belongs_to=instance,
                )
            )

        Account.objects.bulk_create(accounts)
