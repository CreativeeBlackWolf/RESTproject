from django.db import models, transaction
import uuid
from django.forms import ValidationError


class User(models.Model):
    """user: CHAR(128)"""
    user = models.CharField(max_length=128, unique=True, 
                            verbose_name="Username")

    def __str__(self):
        return f"({self.pk}) {self.user}"


class Wallet(models.Model):
    """
    id: UUID PK
    user: FOREIGN KEY (Users)
    name: CHAR(128)
    cash: INTEGER
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, 
                          verbose_name="Wallet ID")
    user = models.ForeignKey(User, on_delete=models.PROTECT, 
                             verbose_name="User")
    name = models.CharField(max_length=128, unique=True, 
                            verbose_name="Wallet name")
    balance = models.IntegerField(default=10000)

    def __str__(self):
        return f"{self.user}: {self.name}"


class Transaction(models.Model):
    """
    from_wallet: FOREIGN KEY (WALLETS) UUID
    to_wallet: FOREIGN KEY (WALLETS) UUID
    whence: CHAR (128)
    date: DATETIME AUTO
    payment: POSITIVE INTEGER
    comment: CHAR(128)
    """
    from_wallet = models.ForeignKey(Wallet, 
                                    on_delete=models.CASCADE, 
                                    related_name="from_wallet",
                                    verbose_name="Initializer Wallet")
    to_wallet = models.ForeignKey(Wallet, 
                                  on_delete=models.CASCADE, 
                                  related_name="to_wallet",
                                  blank=True,
                                  null=True,
                                  verbose_name="Recipient Wallet")
    # откуда/куда пришла транзакция 
    whence = models.CharField(max_length=128,
                              null=True,
                              blank=True,
                              verbose_name="Where/From where the money should be sent/received")
    date = models.DateTimeField(auto_now_add=True)
    payment = models.PositiveIntegerField()
    comment = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # одно из полей 
                # (в кошелёк или куда/откуда) должно быть заполнено
                # но не оба
                name="%(app_label)s_%(class)s_to_wallet_or_not",
                check=(
                    models.Q(to_wallet__isnull=True, whence__isnull=False)
                    |
                    models.Q(to_wallet__isnull=False, whence__isnull=True)
                )
            )
        ]

    class ATMActions:
        DEPOSIT = "ATM Deposit"
        WITHDRAW = "ATM Withdraw"


    @classmethod
    @transaction.atomic
    def make_transaction(cls, from_wallet, payment, to_wallet=None, whence=None, comment=""):
        if not (whence or to_wallet) or (whence and to_wallet):
            return {"error": "one of fields 'from_wallet' or 'whence' must have a value."}
        # если счёта зачисления нет
        if whence:
            if whence is Transaction.ATMActions.DEPOSIT:
                from_wallet.balance += payment
            else:
                if from_wallet.balance < payment:
                    # raise ValueError("not enough money")
                    return {"error": "not enough money"}
                from_wallet.balance -= payment
            from_wallet.save()
            trans = cls.objects.create(
                from_wallet=from_wallet,
                whence=whence,
                payment=payment,
                comment=comment
            )
            return trans
            
        # перевод средств на другой кошелёк
        if to_wallet:
            if from_wallet.balance < payment:
                return {"error": "not enough money"}
            if from_wallet == to_wallet:
                return {"error": "cannot send money to yourself"}
            from_wallet.balance -= payment
            from_wallet.save()
            to_wallet.balance += payment
            to_wallet.save()
            trans = cls.objects.create(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                payment=payment,
                comment=comment
            )
            return trans
