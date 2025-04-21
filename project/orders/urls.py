from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrdersViewSet, OrdersUserViewSet, OrdersUpdateViewSet

router = DefaultRouter()
router.register("orders-user", OrdersUserViewSet,
                basename="orders-user")
router.register("orders", OrdersViewSet,
                basename="orders")
router.register("orders-status", OrdersUpdateViewSet,
                basename="orders-status")
urlpatterns = [
    path('', include(router.urls)),
]
