from rest_framework import serializers
from .models import User, Wallet, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Wallet
        fields = ("pk", "name", "user", "balance")
        read_only_fields = ("pk", "balance")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("from_wallet", "to_wallet", 
                  "whence", "payment", "comment", "id")
        read_only_fields = ("id", )


class TransactionCashActionsSerializer(serializers.ModelSerializer):
    whence = serializers.ChoiceField(
        choices=[Transaction.ATMActions.DEPOSIT, 
                 Transaction.ATMActions.WITHDRAW])

    class Meta:
        model = Transaction
        fields = ("from_wallet", "whence", "payment")
        read_only_fields = ("id", "comment")
