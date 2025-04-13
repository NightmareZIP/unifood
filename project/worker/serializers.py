# подключение библиотек
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Worker
from company.models import Company
from company.serializers import CompanySerializer
from .utils import get_worker


class WorkerCompanySerializer(serializers.ModelSerializer):
    """Класс сериалайзер для применения при регистрации компании
    Мы регистрируем компанию вместе с ее руководителем, и нужно работать одновременно с 2
    моделями
    """

    # Указываем что одним из полей является сериалайзер компании, так мы сможем  получать ее данные
    company = CompanySerializer(required=True)

    class Meta:
        """метаданные класса, указываем, вспомогательный класс основного класса
        """
        #Указываем основную модель для работы
        model = Worker
        #Задаем поля, которые можно читать, но нельзя записывать
        read_only_fields = (
            "created_at",
            "head",
            # "company",
        ),
        #Задаем набор полей, принимаемых сериалайзером
        fields = (
            'name',
            'is_head',
            'last_name',
            'surname',
            'email',
            'contact_phone',
            'country',
            'user_id',
            'created_at',
            'head',
            'company',
        )

    def create(self, validated_data):
        """Создание записи в базе данных

        Args:
            validated_data: данные прошедшие валидацию
        """
        #Забираем данные касающиеся компании
        company = validated_data.pop('company')
        #создаем компанию
        company = Company.objects.create(**company)
        validated_data['company'] = company
        validated_data['is_head'] = True

        #Создаем сотрудника
        worker = Worker.objects.create(**validated_data)
        worker.save()

        return worker


class WorkerSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, required=False)

    class Meta:
        model = Worker
        read_only_fields = (
            "created_at",
            # "head",
            "company",
        ),
        fields = "__all__"

