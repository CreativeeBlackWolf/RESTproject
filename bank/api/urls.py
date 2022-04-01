from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import (TransfersAPIViewSet, UsersAPIViewSet, 
                       WalletsAPIViewSet, 
                       TransactionsAPIViewSet)

app_name = "api"

router = routers.SimpleRouter()
router.register("users", UsersAPIViewSet)
router.register("wallets", WalletsAPIViewSet)
router.register("transactions", TransactionsAPIViewSet)
router.register("transfers", TransfersAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]