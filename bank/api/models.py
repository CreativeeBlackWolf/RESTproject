from django.db import models, transaction
import uuid


class Users(models.Model):
    """user: CHAR(128)"""
    user = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f"({self.pk}) {self.user}"


class Wallets(models.Model):
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


class Transactions(models.Model):
    """
    wallet: FOREIGN KEY (WALLETS) UUID
    date: DATETIME AUTO
    whence: CHAR (128)
    payment: INTEGER
    comment: CHAR(128)
    """
    wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="trans_wallet")
    date = models.DateTimeField(auto_now_add=True)
    whence = models.CharField(max_length=128) # откуда/куда пришла транзакция 
    payment = models.IntegerField()
    comment = models.CharField(max_length=128, null=True, blank=True)

    @classmethod
    def make_transaction(cls, wallet, whence, payment, comment=""):
        if wallet.balance < payment:
            raise ValueError("not enough money")
        
        with transaction.atomic():
            wallet.balance -= payment
            wallet.save()
            transaction = cls.objects.create(
                wallet = wallet,
                whence = whence,
                payment = payment,
                comment = comment
            )
        return wallet, transaction

    @classmethod
    def make_deposit(cls, wallet, payment):
        with transaction.atomic():
            wallet.balance += payment
            wallet.save()
            transaction = cls.objects.create(
                wallet = wallet,
                whence = "ATM",
                payment = payment,
                comment = "Deposit cash"
            )
        return wallet, transaction


class Transfers(models.Model):
    """
    from_wallet: FOREIGN KEY (WALLETS) UUID
    to_wallet: FOREIGN KEY (WALLETS) UUID
    date: DATETIME AUTO
    payment: INTEGER
    comment: CHAR(128)
    """
    from_wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="from_wallet")
    to_wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="to_wallet")
    date = models.DateTimeField(auto_now_add=True)
    payment = models.IntegerField()
    comment = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.to_wallet.user} got {self.payment} from {self.from_wallet.user}"
