from django.forms import model_to_dict
from .serializers import (TransactionsCashActionsSerializer, 
                          UsersSerializer, 
                          WalletsSerializer, 
                          TransfersSerializer, 
                          TransactionsSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .filters import TransactionsFilter, TransfersFilter, WalletsFilter
from .models import Users, Wallets, Transactions, Transfers
from .services import make_transfer


# Create your views here.
class UsersAPIViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @action(methods=["get"], detail=False)
    def get_usernames(self, request):
        usernames = self.queryset
        return Response({"usernames": [i.user for i in usernames]})


class WalletsAPIViewSet(viewsets.ModelViewSet):
    queryset = Wallets.objects.all()
    serializer_class = WalletsSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = WalletsFilter

class TransactionsAPIViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
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

    @action(methods=["post"], detail=False)
    def deposit(self, request):
        serializer = TransactionsCashActionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        view = Transactions.make_ATM_action(**serializer.validated_data, withdraw=False)
        return Response(model_to_dict(view[1]), status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def withdraw(self, request):
        serializer = TransactionsCashActionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        view = Transactions.make_ATM_action(**serializer.validated_data, withdraw=True)
        return Response(model_to_dict(view[1]), status=status.HTTP_201_CREATED)


class TransfersAPIViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    queryset = Transfers.objects.all()
    serializer_class = TransfersSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TransfersFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            return Response({"error": "not enough money"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
