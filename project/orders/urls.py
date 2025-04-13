from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TarifViewSet

router = DefaultRouter()
router.register("tarif", TarifViewSet,
                basename="tarif")

urlpatterns = [
    path('', include(router.urls)),
]
