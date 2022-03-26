from django.db import models
import uuid


class Users(models.Model):
    user = models.CharField(max_length=128)


class Wallets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=128)
    cash = models.IntegerField()


class Transactions(models.Model):
    """
    from_wallet: UUID
    to_wallet: UUID
    payment: INTEGER
    comment: CHAR(128)
    """
    from_wallet = models.UUIDField(blank=False)
    to_wallet = models.UUIDField(blank=False)
    payment = models.IntegerField()
    comment = models.CharField(max_length=128)

