from django.shortcuts import render

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from worker.models import Worker
from menu.models import Menu, MenuItem
from .serializers import OrdersSerializer
from .models import Orders
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class OrdersUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    permission_classes = [AllowAny]
    
    def get_company(self):
        menu = self.request.data.get('menu')
        menu: Menu = Menu.objects.get(id=menu)
        cmp_id = menu.company
        return cmp_id
    def get_menu_prices(self):
        menu_items = self.request.data.get('menu_items')
        id_menu_items = [item.get('id') for item in menu_items]
        db_menu_items: MenuItem = MenuItem.objects.filter(id__in=id_menu_items)
        prices = {item.id: item.discount_price for item in db_menu_items}
        return prices
        
    def perform_create(self, serializer):
        company = self.get_company()
        prices = self.get_menu_prices()
        menu_items:dict = self.request.data.get('menu_items')
        total_cost = sum([round(prices[item.get('id')] * item.get('amount'), 2) for item in menu_items])
        for ind, item in enumerate(menu_items):
            menu_items[ind]['menu_item'] =  MenuItem.objects.get(pk=item.get('id'))
            menu_items[ind]['price'] =  float(MenuItem.objects.get(pk=item.get('id')).discount_price)
        serializer.save(total_cost=total_cost, company=company, prices=prices)
    
    def get_object(self):

        order_uuid = self.request.query_params.get('uuid')
        filter = {'uuid': order_uuid}
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        # d_obj = model_to_dict(obj)
        # full_menu = []
        # for item in d_obj['menu_items']:
        #     price = item.price
        #     menu = model_to_dict(item.menu)
        #     item = model_to_dict(item)
        #     item.update(menu)
        #     item['price'] = price
        #     full_menu.append(item)
        # obj.full_menu_items = full_menu
        return obj
    
class OrdersViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.ListModelMixin):
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()
    def get_company(self):
        user = self.request.user
        worker: Worker = Worker.objects.get(user_id=user)
        cmp_id = worker.company
        return worker, cmp_id
    
    def get_queryset(self):
        worker, cmp_id = self.get_company()
        menu = self.request.query_params.get('menu')
        menu = Menu.objects.get(id=menu)
        return self.queryset.filter(company=cmp_id, menu=menu).order_by('-id')
