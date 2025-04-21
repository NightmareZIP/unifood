from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orders, OrdersItems
from menu.serializers import MenuItemSerializer
import uuid
class OrdersItemsSerializer(serializers.ModelSerializer):
    """Класс сериалайзера блюд у заказов
    """
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)
    class Meta:
        model = OrdersItems
        read_only_fields = (    
        ),
        extra_kwargs = {'order': {'required': False,}}
        fields = '__all__'
    
    
class OrdersSerializer(serializers.ModelSerializer):
    """Класс сериалайзера заказов
    """
    # full_menu_items = serializers.ListField(read_only=True)

    menu_items = OrdersItemsSerializer(source="ordersitems_set", many=True)
    class Meta:
        #Сущность
        model = Orders
        #поля доступные только для чтения
        read_only_fields = (
            'created_at',
            'uuid',
        )
        extra_kwargs = {'status': {'required': False, 'default':'new'},
                        'customer_name': {'required': False,},
                        'customer_comment': {'required': False,},
                        'owner_comment': {'required': False},
                        'total_cost': {'required': False},
                        'uuid': {'required': False},
                        
                        }
        
        #Список полей, обрабатывыемых сериалайзером
        fields = '__all__'
    
    
    def create(self, validated_data):
        prices = validated_data.pop('prices')
        menu_items = validated_data.pop('ordersitems_set')
        for ind, menu in enumerate(menu_items):
            menu_items[ind]['price'] = prices[menu['menu_item'].id]
        validated_data['uuid'] = uuid.uuid4()
        order = Orders.objects.create(**validated_data)
        for menu_item in menu_items:
            OrdersItems.objects.create(order=order, **menu_item)
        return order
