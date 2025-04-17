from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu, MenuItem


class MenuSerializer(serializers.ModelSerializer):
    """Класс сериалайзера компании
    """
    class Meta:
        #Сущность
        model = Menu
        #поля доступные только для чтения
        read_only_fields = (
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = "__all__"
        extra_kwargs = {'description': {'required': False},
                        'company': {'required': False}
                        }


class MenuItemSerializer(serializers.ModelSerializer):
    """Класс сериалайзера компании
    """

    discount_price = serializers.DecimalField(required=False, max_digits=6, decimal_places=2)
    def validate(self, data):
            discount = data['discount']
            price = data['price']
            if not (0 < discount < 99):
                raise serializers.ValidationError('Скидка должна быть больше 0 и меньше 99')
            if not (0 < price):
                raise serializers.ValidationError('Цена не может быть отрицательной и содержать более 2 знаков после запятой')
            return data

    class Meta:
        #Сущность
        model = MenuItem
        #поля доступные только для чтения
        read_only_fields = (
            'discount_price',
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = "__all__"
        extra_kwargs = {'discount': {'required': False},
                        'discount_start': {'required': False, 'format': '%Y-%m-%d'},
                        'discount_end': {'required': False, 'format': '%Y-%m-%d'},
                        'company': {'required': False},
                        }
