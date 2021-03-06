from django.forms import ValidationError
from .serializers import (TransactionCashActionsSerializer, 
                          UserSerializer, 
                          WalletSerializer, 
                          TransactionSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .filters import TransactionFilter, WalletFilter
from .models import User, Wallet, Transaction


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WalletAPIViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = WalletFilter


class TransactionAPIViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backend = (DjangoFilterBackend, )
    filterset_class = TransactionFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = Transaction.make_transaction(**serializer.validated_data)
        if isinstance(result, dict):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=False)
    def ATM_action(self, request):
        serializer = TransactionCashActionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        result = Transaction.make_transaction(**serializer.validated_data)
        if isinstance(result, dict):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
