from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from .services import *


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
    
    def get_queryset(self):
        if 'user' in self.kwargs:
            return Wallets.objects.filter(user=self.kwargs['user'])
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
        serializer = WalletsSerializer(data = {**request.data, 'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"wallet": serializer.data})

    @action(methods=['get'], detail=True)
    def get_by_name(self, request, user=None):
        try:
            check_args(request.GET, "wallet_name")
        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"wallet": get_wallet_dict_by_name(request.GET["wallet_name"])})


    @action(methods=['post'], detail=True)
    def delete_wallet(self, request, user=None):
        try:
            check_args(request.data, "wallet_name")
        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        wallet = get_wallet_by_name(request.data["wallet_name"])
        wallet.delete()

        return Response({"success": True})


class TransactionsAPIViewSet(GenericViewSet, 
                             mixins.ListModelMixin, 
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin):
    # lookup_field = "from_wallet"
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if "limit" in request.GET:
            try:
                return Response(serializer.data[:int(request.GET["limit"])])
            except ValueError:
                return Response({"error": "limit parameter must be integer"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(methods=["post"], detail=False)
    def make_transaction(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            return Response({"error": "not enough money"}, 
                             status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_transactions(self, request):
        try:
            check_args(request.GET, "wallet_name")
        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
