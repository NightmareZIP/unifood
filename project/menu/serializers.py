from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu


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
