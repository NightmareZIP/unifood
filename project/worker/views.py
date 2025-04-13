from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .serializers import WorkerSerializer, WorkerCompanySerializer
from company.models import Company
from .utils import get_worker
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class WorkerCompanyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Класс для обработки создания компании и руководителя
    явно задаем через примеси, что класс служит только для создания записей

    Args:
        mixins: примеси класса GenericViewSet
    """
    # Задаем серилайзер
    serializer_class = WorkerCompanySerializer
    # Задаем сущность для работы
    queryset = Worker.objects.all()
    # Выполнение создания записи (post запрос)

    def perform_create(self, serializer):
        serializer.save()


class WorkerViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet,):
    """Класс для работы с сщуность Работника, через миксины задаем, что он может выполнять
    полный CRUD набор (создание, извлечение, получение, уждаление)

    Args:
        mixins: Миксины

    Raises:
        PermissionDenied: при отсутствии разрешения, возбуждаем исключение

    """
    # устанавливаем сериалайзер
    serializer_class = WorkerSerializer
    # задаем сущность для работы
    queryset = Worker.objects.all()

    def get_object(self):
        """получение конкретной записи из бд на основе id передаваемого при запросе

        Returns:
            _type_: _description_
        """
        # фильтруем данные на основе фильтра
        queryset = self.filter_queryset(Worker.objects.all())
        # Ищем в url id пердаваемый в url
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        # Проверяем его наличие
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        # Записываем его в фильтр
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        # Получаем в БД запись с id либо возвращаем ошибку 404
        obj = get_object_or_404(queryset, **filter_kwargs)

        # Проверяем права
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        """Указываем, что нужно получать только запись сотрудника, отправившего запрос
        """
        worker_id = get_worker(self.request.user)
        return self.queryset.filter(pk=worker_id)

    def perform_create(self, serializer):
        """Обработка запроса на создание Работника

        Args:
            serializer
        """
        # Получаем id компании из запроса
        company_id = self.request.data['company']
        # Получаем главу компании
        company = Company.objects.get(id=company_id)
        head = Worker.objects.all().get(is_head=True, company=company_id)
        # Вызываем метод сериалайзера по добавлению записи, указывая руководитя и данные компании
        serializer.save(head=head,  company=company)

    def perform_update(self, serializer):
        """Изменение данных Работника

        Args:
            serializer 
        Raises:
            PermissionDenied:
        """
        # получаем запись в БД о данном работнике
        worker_id = get_worker(self.request.user)
        obj = self.get_object()

        # Если работник пытается изменить не свои данные, вызвается ошибка
        if worker_id != obj.id:
            raise PermissionDenied('Wrong object owner')

        serializer.save()

    @action(detail=False)
    def get_workers(self, request):
        """Получение коллег работника (сотрудники той же компании)
        Декотор @action сообщает, что это метод собственный метод, обрабатывающий
        запрос

        Args:
            request (_type_): объект запрос

        """
        q_set = self.get_queryset()
        company = self.request.user.worker_user.company
        workers = Worker.objects.all().filter(company=company)
        # Проверка прав
        self.check_object_permissions(self.request, workers)
        serializer = self.get_serializer(workers, many=True)
        # Возвращаем в ответе сериализованные данные
        return Response(serializer.data)
