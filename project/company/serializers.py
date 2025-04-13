from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company
from worker.models import Worker
import datetime

class CompanySerializer(serializers.ModelSerializer):
    """Класс сериалайзера компании
    """
    class Meta:
        #Сущность
        model = Company
        #поля доступные только для чтения
        read_only_fields = (
            "tarif",    
        )
        #Список полей, обрабатывыемых сериалайзером
        fields = (
            'id',
            'name',
            'country',
            'place',
            'contact_person',
            'contact_phone',
            'email',
            'inn',
            'description',
            'tarif',
            'tarif_date',
            'logo',
        )
        extra_kwargs = {'description': {'required': False},
                        'logo': {'required': False},
                        'tarif_date': {'format': '%d-%m-%Y'}
                        }

class CompanyTarifSerializer(serializers.ModelSerializer):
    """Класс сериалайзера компании
    """
    months = serializers.IntegerField(required=False)
    class Meta:
        #Сущность
        model = Company
        #Список полей, обрабатывыемых сериалайзером
        write_only_fields = ('tarif')
        fields = (
            'id',
            'tarif',
            'months',
        )
    def validate(self, attrs):
        if attrs['months'] not in [1, 3, 6, 12]:
            raise serializers.ValidationError({'error': 'Срок тарифа должен быть 1, 3, 6 или 12 месяцев'})
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        tarif = validated_data['tarif']
        months = validated_data.pop('months')
        instance.tarif = tarif
        current_datetime = datetime.datetime.now()
        instance.tarif_date = current_datetime + datetime.timedelta(days=months*30)
        instance.save()
        return instance