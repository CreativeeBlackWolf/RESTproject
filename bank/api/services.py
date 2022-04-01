from django.shortcuts import get_object_or_404
from .models import Transactions, Transfers, Wallets
from django.forms import model_to_dict
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

def action_cash(wallet, cash, withdrawal = False) -> Transactions:
    with transaction.atomic():
        wallet.balance = wallet.balance + cash if not withdrawal else wallet.balance + cash
        wallet.save()

        transfer = Transactions.objects.create(
            from_wallet = wallet,
            to_wallet = wallet,
            payment = cash,
            comment = "Cash withdrawal" if withdrawal else "Cash depositing"
        )
    return transfer


def get_wallet_dict_by_name(wallet_name):
    wallet = get_object_or_404(Wallets, wallet_name=wallet_name)
    dict_wallet = model_to_dict(wallet)
    dict_wallet["uuid"] = wallet.pk
    return dict_wallet

def get_wallet_by_name(wallet_name):
    return get_object_or_404(Wallets, wallet_name=wallet_name)

def check_args(data: dict, *args):
    """Raises TypeError if given arguments are not in data dictionary."""
    # print(data.dict(), args, not ({*args} <= set(data.dict())))
    if not ({*args} <= set(data.dict())):
        raise TypeError("some arguments are missing: {0}".format(", ".join(args)))

    
