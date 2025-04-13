from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from .serializers import TarifSerializer
from tarif.models import Tarif
from rest_framework import generics
from django.core.exceptions import PermissionDenied


class TarifViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     ):
    serializer_class = TarifSerializer
    queryset = Tarif.objects.all()