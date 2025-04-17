from django.shortcuts import render

from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAuthenticated, BasePermission ,SAFE_METHODS
from django.contrib.auth.models import User

from .serializers import MenuSerializer, MenuItemSerializer
from .models import Menu, MenuItem
from worker.models import Worker
from tarif.models import Tarif
from rest_framework import generics
from django.core.exceptions import PermissionDenied

class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

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

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    pagination_class = ResultsSetPagination
    permission_classes = [IsAuthenticated|ReadOnlyPermission]
    def get_queryset(self):
        """
        Get the queryset based on the user's company ID.

        Returns:
            QuerySet: The queryset filtered based on the user's company ID, or False if the worker is not found.
        """
        # worker, cmp_id = self.get_company()
        menu_id = self.request.query_params.get('menu')
        tarif = Menu.objects.get(pk=menu_id).company.tarif
        if not tarif:
            return False
        limit: Tarif = tarif.max_menu
        self.pagination_class.page_size = limit
        return self.queryset.filter(menu=menu_id).order_by('id')

    def get_company(self):
        user = self.request.user
        worker: Worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company
        return worker, cmp_id

    def perform_create(self, serializer):
        worker, company_id = self.get_company()
        menu_id = self.request.data.get('menu')
        if worker:
            menu =  Menu.objects.filter(id=menu_id, company=company_id)[0:1]
            if not menu:
                return False
        serializer.save()
    
    def perform_update(self, serializer):
        worker, company_id = self.get_company()
        menu_id = self.request.data.get('menu')
        if worker:
            menu =  Menu.objects.filter(id=menu_id, company=company_id)[0:1]
            if not menu:
                return False
        serializer.save()