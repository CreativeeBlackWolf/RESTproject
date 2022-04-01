from django.contrib import admin
from .models import (Transfers, Users, Wallets, Transactions)
# Register your models here.
admin.site.register(Users)
admin.site.register(Wallets)
admin.site.register(Transactions)
admin.site.register(Transfers)
