from django.contrib import admin

from .models import Orders, OrdersItems

admin.site.register(Orders)
admin.site.register(OrdersItems)