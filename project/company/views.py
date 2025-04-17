from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import CompanySerializer, CompanyTarifSerializer
from .models import Company
from worker.models import Worker
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action

class CompanyBase(viewsets.GenericViewSet):
    queryset = Company.objects.all()

    def get_queryset(self):
        """
        Get the queryset based on the user's company ID.

        Returns:
            QuerySet: The queryset filtered based on the user's company ID, or False if the worker is not found.
        """
        # company_id = self.request.data['company']

        user = self.request.user
        worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company.id

        if worker:
            return self.queryset.filter(id=cmp_id)
        return False
    
    def _check_user(self):
        user = self.request.user
        worker = Worker.objects.get(user_id=user)
        cmp_head = worker.is_head

        cmp_id = int(self.request.parser_context['kwargs']['pk'])
        if not cmp_head or worker.company.id != cmp_id:
            raise PermissionDenied('Wrong object owner')
            
    
class CompanyViewSet(CompanyBase, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     ):
    serializer_class = CompanySerializer
       
    def perform_update(self, serializer):
        self._check_user()
        serializer.save()


class CompanyTarifViewSet(CompanyBase, mixins.UpdateModelMixin):
    serializer_class = CompanyTarifSerializer
    
    def perform_update(self, serializer):
        self._check_user()
        serializer.save()