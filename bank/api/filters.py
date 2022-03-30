from corsheaders import django
import django_filters
from .models import Transactions

class TransactionsFilter(django_filters.FilterSet):
    max_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="lte")
    min_payment = django_filters.NumberFilter(field_name="payment", lookup_expr="gte")
    from_wallet_name = django_filters.CharFilter(field_name="from_wallet__wallet_name")
    to_wallet_name = django_filters.CharFilter(field_name="to_wallet__wallet_name")

    class Meta:
        model = Transactions
        fields = ("from_wallet", "to_wallet", "payment", "comment")
