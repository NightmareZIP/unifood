# подключение библиотек
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Worker
from company.models import Company
from company.serializers import CompanySerializer
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()

class WorkerCompanySerializer(serializers.ModelSerializer):
    """Класс сериалайзер для применения при регистрации компании
    Мы регистрируем компанию вместе с ее руководителем, и нужно работать одновременно с 2
    моделями
    """

    # Указываем что одним из полей является сериалайзер компании, так мы сможем  получать ее данные
    company = CompanySerializer(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        """метаданные класса, указываем, вспомогательный класс основного класса
        """
        #Указываем основную модель для работы
        model = Worker
        #Задаем поля, которые можно читать, но нельзя записывать
        read_only_fields = (
            "created_at",
            "head",
            "user_id",
            # "company",
        )
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
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True,},
            'username': {'write_only': True,},

            }


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
        user = UserModel.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.pop('password'),
        )
        #Создаем сотрудника
        worker = Worker.objects.create(**validated_data)
        validated_data['user_id'] = user
        worker.save()
        return worker


class WorkerSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    class Meta:
        model = Worker
        read_only_fields = (
            "id",
            "created_at",
            # "head",
            "company",
            "user_id",
        ) 
        fields = (
            "id",
            "name",
            "last_name",
            "surname",
            "email",
            "contact_phone",
            "country",
            "user_id",
            "created_at",
            "head",
            "company",
            "is_head",
            "password",
            "username",
            "company",
        )
        extra_kwargs = {
            'password': {'write_only': True,},
            'username': {'write_only': True,},
            
        }
    def create(self, validated_data):
        #создаем компанию
        user = UserModel.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.get('username'),
            password=validated_data.pop('password'),
        )
        #Создаем сотрудника
        validated_data['user_id'] = user
        worker = Worker.objects.create(**validated_data)
        worker.save()
        return worker


# class UserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     def create(self, validated_data):

#         user = UserModel.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#         )

#         return user

#     class Meta:
#         model = UserModel
#         # Tuple of serialized model fields (see link [2])
#         fields = ( "id", "username", "password", )