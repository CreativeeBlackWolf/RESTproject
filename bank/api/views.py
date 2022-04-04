from django.forms import model_to_dict
from .serializers import (TransactionCashActionsSerializer, 
                          UserSerializer, 
                          WalletSerializer, 
                          TransactionSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .filters import TransactionsFilter, WalletsFilter
from .models import Users, Wallets, Transactions


class UsersAPIViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class WalletsAPIViewSet(viewsets.ModelViewSet):
    queryset = Wallets.objects.all()
    serializer_class = WalletSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = WalletsFilter

class TransactionsAPIViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    filter_backend = (DjangoFilterBackend, )
    filterset_class = TransactionsFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            Transactions.make_transaction(**serializer.validated_data)
        except ValueError:
            return Response({"error": "not enough money"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
