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
    from_wallet_name = serializers.CharField(source="from_wallet.name")
    to_wallet_name = serializers.CharField(source="to_wallet.name", allow_null=True)
    class Meta:
        model = Transaction
        fields = ("from_wallet", "from_wallet_name", "to_wallet", 
                  "to_wallet_name", "whence", "date", 
                  "payment", "comment", "id")
        read_only_fields = ("id", )


class TransactionCashActionsSerializer(serializers.ModelSerializer):
    whence = serializers.ChoiceField(
        choices=[Transaction.DEPOSIT, 
                 Transaction.WITHDRAW])

    class Meta:
        model = Transaction
        fields = ("from_wallet", "whence", "payment")
        read_only_fields = ("id", "comment")
