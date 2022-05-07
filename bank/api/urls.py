from django.urls import path, include
from rest_framework import routers
from .views import (UserAPIViewSet,
                    WalletAPIViewSet,
                    TransactionAPIViewSet)

app_name = "api"

router = routers.SimpleRouter()
router.register("users", UserAPIViewSet)
router.register("wallets", WalletAPIViewSet)
router.register("transactions", TransactionAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
