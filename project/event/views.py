from django.shortcuts import render
from datetime import date, datetime, timedelta
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from worker.utils import get_worker
from rest_framework.decorators import action
from .serializers import EventTypeSerializer, EventSerializer
from .models import Event, EventType
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response


class EventViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """_summary_
        Класс представление для работы с событиями
    Args:
        mixins (_type_): _description_
        mixins (_type_): _description_
        mixins (_type_): _description_
        mixins (_type_): _description_
        viewsets (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def head_or_worker(self):
        """Проверяем был ли предан id работника в запросе

        Returns:
            _type_: _description_
        """
        user_id = self.request.query_params.get('user_id')
        print(self.request.query_params)

        if not user_id and 'user_id' in self.request.data:
            user_id = self.request.data['user_id']
            # del self.request.data['user_id']
            print('LLL', self.request.data)

        return user_id

    def get_queryset(self, read = False):

        user_id = self.head_or_worker()
        print(user_id)
        if user_id:
            worker = Worker.objects.all()
            worker = worker.get(id=user_id)
            check = [worker.id]
            if worker.head:
                check.append(worker.head.id)
            if (self.request.user.worker_user.id not in check and not read):
                raise PermissionDenied(
                    'Вы можете изменять только свой календарь и своих прямых подчиненных')
            else:
                return self.queryset.filter(created_for=user_id)

        else:
            worker_id = get_worker(self.request.user)
            # TODO Добавить обработку по url дял начальника
            if worker_id:
                return self.queryset.filter(created_for=worker_id)
        return False

    @action(detail=False)
    def get_events(self, request):
        """Получение событий работника, при этом в запрос попадают так же периодические события

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Получим непиродические события

        q_set = self.get_queryset(read = True)
        date_from = self.request.query_params.get('date_from')
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = self.request.query_params.get('date_to')
        date_to = datetime.strptime(date_to,  "%Y-%m-%d")

        not_period = q_set.filter(
            date_from__gte=date_from, date_to__lte=date_to, period=0)

        # Получим все периодические события
        period = q_set.filter(~Q(period=0), date_to__lte=date_to)
        period_copy = period.all()
        delta = date_to - date_from   # returns timedelta
        days = []
        for i in range(delta.days + 1):
            day = date_from + timedelta(days=i)
            days.append(day)
        for event in period:
            excl = True
            for day in days:
                day_from = event.date_from
                # Убираем Timezone django
                dif = day_from.replace(tzinfo=None) - day
                if dif.days % event.period == 0:
                    excl = False
                    break
                    print(event.id)
            if excl:
                period_copy.exclude(id=event.id)

        event_combine = period_copy | not_period
        self.check_object_permissions(self.request, event_combine)

        serializer = self.get_serializer(event_combine, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # print(self.request.data['event_type'])
        # event_type = EventType.objects.get(id=event_type)
        user_id = self.head_or_worker()
        if user_id:
            created_for = Worker.objects.get(id=user_id)
        else:
            created_for = Worker.objects.get(user_id=self.request.user)

        created_by = Worker.objects.get(user_id=self.request.user)

        serializer.save(created_by=created_by,
                        created_for=created_for)

    def perform_update(self, serializer):
        # print(self.request.data['event_type'])
        # event_type = EventType.objects.get(id=event_type)
        user_id = self.head_or_worker()
        if user_id:
            created_for = Worker.objects.get(id=user_id)
        else:
            created_for = Worker.objects.get(user_id=self.request.user)

        created_by = Worker.objects.get(user_id=self.request.user)

        serializer.save(created_by=created_by,
                        created_for=created_for,)


class EventTypeViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()
