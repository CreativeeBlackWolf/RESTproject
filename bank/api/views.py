from django.shortcuts import get_object_or_404
from django.forms import model_to_dict
from django.http import response
from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import *


# Create your views here.
class UsersAPIViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @action(methods=["get"], detail=False)
    def get_usernames(self, request):
        usernames = self.queryset
        return Response({"usernames": [i.user for i in usernames]})


class WalletsAPIViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    lookup_field = "user"
    queryset = Wallets.objects.all()
    serializer_class = WalletsSerializer
    
    def convert_to_dict(self, wallet: Wallets) -> dict:
        wallet_dict = model_to_dict(wallet)
        wallet_dict["uuid"] = wallet.pk
        return wallet_dict
    
    def get_queryset(self):
        if 'user' in self.kwargs:
            return Wallets.objects.filter(user=self.kwargs['user'])
        else:
            return Wallets.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if "limit" in request.GET:
            try:
                return Response(serializer.data[:int(request.GET["limit"])])
            except ValueError:
                return Response({"error": "limit parameter must be integer"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def create_wallet(self, request, user=None):
        serializer = WalletsSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"wallet": serializer.data})

    @action(methods=['get'], detail=True)
    def get_by_name(self, request, user=None):
        if "wallet_name" not in request.GET:
            return Response({"error": "wallet_name field is required"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        wallet_name = request.GET["wallet_name"]
        wallet = get_object_or_404(Wallets, user=user, wallet_name=wallet_name)
        wallet_json = self.convert_to_dict(wallet)
        return Response({"wallet": wallet_json})

    @action(methods=['post'], detail=True)
    def delete_wallet(self, request, user=None):
        wallet_name = request.data.get("wallet_name")
        if not wallet_name:
            return Response({"error": "wallet_name field is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        wallet = get_object_or_404(Wallets, user=user, wallet_name=wallet_name)
        wallet_json = self.convert_to_dict(wallet)
        wallet.delete()

        return Response({"wallet": wallet_json})


class TransactionsAPIViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
