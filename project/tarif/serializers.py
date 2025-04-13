from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tarif


class TarifSerializer(serializers.ModelSerializer):
    """Класс сериалайзера тарифов
    """
    class Meta:
        #Сущность
        model = Tarif
        #поля доступные только для чтения
        read_only_fields = (
            
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = "__all__"
