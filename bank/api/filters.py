from dataclasses import field
import django_filters
from .models import Transactions, Transfers, Wallets

class TransfersFilter(django_filters.FilterSet):
    max_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="lte")
    min_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="gte")
    from_wallet_name = django_filters.CharFilter(field_name="from_wallet__wallet_name")
    to_wallet_name = django_filters.CharFilter(field_name="to_wallet__wallet_name")

    class Meta:
        model = Transfers
        fields = ("from_wallet", "to_wallet", "payment", "comment")

class TransactionsFilter(django_filters.FilterSet):
    max_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="lte")
    min_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="gte")
    wallet_name = django_filters.CharFilter(field_name="wallet__wallet_name")

    class Meta:
        model = Transactions
        fields = ("wallet", "whence", "payment", "comment")

class WalletsFilter(django_filters.FilterSet):
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")
    class Meta:
        model = Wallets
        fields = ("wallet_name", "user", "balance")
