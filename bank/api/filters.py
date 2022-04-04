import django_filters
from .models import Transaction, Wallet

class TransactionsFilter(django_filters.FilterSet):
    max_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="lte")
    min_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="gte")

    class Meta:
        model = Transaction
        fields = ("from_wallet", "whence", "payment", "comment")

class WalletsFilter(django_filters.FilterSet):
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    class Meta:
        model = Wallet
        fields = ("name", "user", "balance")
