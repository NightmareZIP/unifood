from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orders, OrdersItems


class OrderSerializer(serializers.ModelSerializer):
    """Класс сериалайзера тарифов
    """
    class Meta:
        #Сущность
        model = Orders
        #поля доступные только для чтения
        read_only_fields = (
            "company",
            'created_at',
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = '__all__'
