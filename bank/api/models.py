from django.db import models, transaction
import uuid


class User(models.Model):
    """user: CHAR(128)"""
    user = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"({self.pk}) {self.user}"


class Wallet(models.Model):
    """
    id: UUID PK
    user: FOREIGN KEY (Users)
    name: CHAR(128)
    cash: INTEGER
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("Users", on_delete=models.PROTECT)
    name = models.CharField(max_length=128, unique=True)
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
                                    related_name="from_wallet")
    to_wallet = models.ForeignKey(Wallet, 
                                  on_delete=models.CASCADE, 
                                  related_name="to_wallet",
                                  blank=True,
                                  null=True)
    whence = models.CharField(max_length=128,
                              null=True,
                              blank=True) # откуда/куда пришла транзакция 
    date = models.DateTimeField(auto_now_add=True)
    payment = models.PositiveIntegerField()
    comment = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # одно из полей 
                # (в кошелёк или куда/откуда) должно быть заполнено
                name = "%(app_label)s_%(class)s_to_wallet_or_not",
                check = (
                    models.Q(to_wallet__isnull=True, whence__isnull=False)
                    |
                    models.Q(to_wallet__isnull=False, whence__isnull=True)
                )
            )
        ]

    @classmethod
    @transaction.atomic
    def make_transaction(cls, wallet, whence, payment, comment=""):
        if wallet.balance < payment:
            raise ValueError("not enough money")
        wallet.balance -= payment
        wallet.save()
        transaction = cls.objects.create(
            wallet = wallet,
            whence = whence,
            payment = payment,
            comment = comment
        )
        return wallet, transaction

    # @classmethod
    # @transaction.atomic
    # def make_ATM_action(cls, wallet, payment, withdraw=False):
    #     wallet.balance = wallet.balance + payment if not withdraw else wallet.balance - payment
    #     wallet.save()
    #     transaction = cls.objects.create(
    #         wallet = wallet,
    #         whence = "ATM",
    #         payment = payment,
    #         comment = "Deposit cash" if not withdraw else "Withdraw cash"
    #     )
    #     return wallet, transaction


# class Transfer(models.Model):
#     """
#     from_wallet: FOREIGN KEY (WALLET) UUID
#     to_wallet: FOREIGN KEY (WALLET) UUID
#     date: DATETIME AUTO
#     payment: INTEGER
#     comment: CHAR(128)
#     """
#     from_wallet = models.ForeignKey(Wallet, 
#                                     on_delete=models.CASCADE, 
#                                     related_name="from_wallet")
    # to_wallet = models.ForeignKey(Wallet, 
    #                               on_delete=models.CASCADE, 
    #                               related_name="to_wallet",
    #                               blank=True)
    # whence = models.CharField(max_length=128,
    #                           blank=True,
    #                           default="To wallet")
#     date = models.DateTimeField(auto_now_add=True)
#     payment = models.IntegerField()
#     comment = models.CharField(max_length=128, null=True, blank=True)

#     def __str__(self):
#         return f"{self.to_wallet.user} got {self.payment} from {self.from_wallet.user}"
