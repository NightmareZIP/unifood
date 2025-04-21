from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrdersViewSet, OrdersUserViewSet

router = DefaultRouter()
router.register("orders-user", OrdersUserViewSet,
                basename="orders-user")
router.register("orders", OrdersViewSet,
                basename="orders")

urlpatterns = [
    path('', include(router.urls)),
]
