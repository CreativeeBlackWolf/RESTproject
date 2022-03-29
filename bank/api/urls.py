from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import (UsersAPIViewSet, 
                       WalletsAPIViewSet, 
                       TransactionsAPIViewSet)

app_name = "api"

router = routers.SimpleRouter()
router.register("users", UsersAPIViewSet)
router.register("wallets", WalletsAPIViewSet)
router.register("transactions", TransactionsAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]