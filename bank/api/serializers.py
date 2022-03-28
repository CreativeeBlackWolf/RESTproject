from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class WalletsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    
    class Meta:
        model = Wallets
        fields = ("pk", "wallet_name", "user", "cash")
        # read_only_fields = ["cash"]

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ("from_wallet", "to_wallet", "payment", "comment", "id")