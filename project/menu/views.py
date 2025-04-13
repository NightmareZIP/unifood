from django.shortcuts import render

from rest_framework import viewsets, pagination
from django.contrib.auth.models import User

from .serializers import MenuSerializer
from .models import Menu
from worker.models import Worker
from tarif.models import Tarif
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class ResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000

class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        """
        Get the queryset based on the user's company ID.

        Returns:
            QuerySet: The queryset filtered based on the user's company ID, or False if the worker is not found.
        """
        # company_id = self.request.data['company']

        worker, cmp_id = self.get_company()
        limit: Tarif = worker.company.tarif.max_menu
        self.pagination_class.page_size = limit
        if worker:
            return self.queryset.filter(company=cmp_id).order_by('id')
        return False

    def get_company(self):
        user = self.request.user
        worker: Worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company
        return worker, cmp_id

    def perform_create(self, serializer):
        _, company_id = self.get_company()
        serializer.save(company=company_id)
    
    def perform_update(self, serializer):
        _, company_id = self.get_company()
        serializer.save(company=company_id)
