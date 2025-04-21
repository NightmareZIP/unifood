from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import TarifSerializer
from tarif.models import Tarif
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from worker.models import Worker
from menu.models import Menu
from rest_framework.permissions import AllowAny
#Нужно только получение элементов и списка
class TarifViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     ):
    serializer_class = TarifSerializer
    queryset = Tarif.objects.all().order_by('id')
    permission_classes = [AllowAny]

    def get_company(self):
        user = self.request.user
        worker: Worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company
        return worker, cmp_id
    
    def get_object(self):
        if menu:= self.request.query_params.get('menu'):
            company = Menu.objects.get(id=menu).company
            tarif = company.tarif.id
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            self.kwargs[lookup_url_kwarg] = tarif
        else:
            _, company = self.get_company()
        object = super().get_object()
        object.tarif_date = company.tarif_date
        return object