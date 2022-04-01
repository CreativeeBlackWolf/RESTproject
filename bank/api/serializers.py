from rest_framework import serializers
from .models import (Users, Wallets, Transactions, Transfers)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class WalletsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model = Wallets
        fields = ("pk", "wallet_name", "user", "balance")
        read_only_fields = ("pk", "balance")

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ("wallet", "whence", "payment", "comment", "id")
        read_only_fields = ("id", )

class TransfersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfers
        fields = ("from_wallet", "to_wallet", "payment", "comment", "id")
        read_only_fields = ("id", )
