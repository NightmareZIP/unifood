from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MenuViewSet, MenuItemViewSet

router = DefaultRouter()
router.register("menu", MenuViewSet,
                basename="menu")
router.register("menu-items", MenuItemViewSet,
                basename="menu-items")

urlpatterns = [
    path('', include(router.urls)),
]
