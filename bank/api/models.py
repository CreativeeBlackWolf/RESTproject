from django.db import models
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
    wallet_name: CHAR(128)
    cash: INTEGER
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=128, unique=True)
    cash = models.IntegerField(default=10000)

    def __str__(self):
        return f"{self.user}: {self.wallet_name}"


class Transactions(models.Model):
    """
    from_wallet: UUID
    to_wallet: UUID
    payment: INTEGER
    comment: CHAR(128)
    """
    from_wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="from_wallet")
    to_wallet = models.ForeignKey(Wallets, on_delete=models.CASCADE, related_name="to_wallet")
    payment = models.IntegerField()
    comment = models.CharField(max_length=128)

