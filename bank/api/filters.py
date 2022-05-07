import django_filters
from .models import Transaction, Wallet


class TransactionFilter(django_filters.FilterSet):
    max_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="lte")
    min_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="gte")
    from_wallet_name = django_filters.CharFilter(field_name="from_wallet__name")
    to_wallet_name = django_filters.CharFilter(field_name="to_wallet__name")
    from_user = django_filters.CharFilter(field_name="from_wallet__user")
    to_user = django_filters.CharFilter(field_name="to_wallet__user")

    class Meta:
        model = Transaction
        fields = ("from_wallet", "to_wallet", "whence", "payment", "comment")


class WalletFilter(django_filters.FilterSet):
    max_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="lte")
    min_balance = django_filters.NumberFilter(field_name="balance", lookup_expr="gte")

    class Meta:
        model = Wallet
        fields = ("name", "user", "balance")
