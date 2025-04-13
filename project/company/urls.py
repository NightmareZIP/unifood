from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, CompanyTarifViewSet

router = DefaultRouter()
router.register("company", CompanyViewSet,
                basename="company")
router.register("company-tarif", CompanyTarifViewSet,
                basename="company-tarif")

urlpatterns = [
    path('', include(router.urls)),
]
