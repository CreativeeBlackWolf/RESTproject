from .models import Transactions, Transfers
from django.db import transaction


def make_transfer(from_wallet, to_wallet, payment, comment="") -> Transactions:
    if from_wallet == to_wallet:
        raise AttributeError("cannot send money to yourself")
    if from_wallet.balance < payment:
        raise ValueError("not enough money")

    with transaction.atomic():
        from_balance = from_wallet.balance - payment
        from_wallet.balance = from_balance
        from_wallet.save()

        to_balance = to_wallet.balance + payment
        to_wallet.balance = to_balance
        to_wallet.save()

        transfer = Transfers.objects.create(
            from_wallet = from_wallet,
            to_wallet = to_wallet,
            payment = payment,
            comment = comment
        )
    
    return transfer
