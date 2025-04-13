from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import EventViewSet, EventTypeViewSet

router = DefaultRouter()
router.register("event", EventViewSet,
                basename="event")
router.register("eventtype", EventTypeViewSet, basename="eventtype")

urlpatterns = [
    path('', include(router.urls)),
]
