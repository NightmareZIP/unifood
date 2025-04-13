# подключаем библиотеки
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkerCompanyViewSet, WorkerViewSet
# Создаем объект роутера
router = DefaultRouter()
# Регистрируем пути в роутере для представления, по принципу REST
router.register("workercompany", WorkerCompanyViewSet,
                basename="workercompany")
router.register("workers", WorkerViewSet, basename="workers")
#добавляем пути в специальный список
urlpatterns = [
    path('', include(router.urls)),
]
