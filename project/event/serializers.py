from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventType
from company.models import Company
from worker.models import Worker
from worker.serializers import WorkerSerializer

from company.serializers import CompanySerializer

from worker.utils import get_worker


class EventTypeSerializer(serializers.ModelSerializer):
    """_summary_
        Серриалайзер для ReadOnly
    Args:
        serializers (_type_): _description_
    """

    class Meta:
        model = EventType
        # read_only_fields = (
        #     'name',
        #     'id',
        #     'color',
        # )
        fields = (
            'id',
            'color',
            'name',
        )
        extra_kwargs = {'id': {'read_only': False}}


class EventSerializer(serializers.ModelSerializer):
    event_type = EventTypeSerializer(required=True)
    created_by = WorkerSerializer(read_only=True)
    created_for = WorkerSerializer(read_only=True, required=False)
    # user_id = serializers.IntegerField(write_only=True,  required=False)

    class Meta:
        model = Event
        # extra_kwargs = {
        #     'created_for': {'read_only': True},
        #     'created_by': {'read_only': True},

        # }
        read_only_fields = (
            "id",
            "created_at",
            "created_for",
            "created_by",
        )
        fields = (
            "id",
            "created_at",
            'event_type',
            'created_by',
            'created_for',
            'date_from',
            'date_to',
            'event_name',
            'period',
            'comment',
            # 'user_id',
        )

    def create(self, validated_data):
        print(validated_data)
        event_type = validated_data['event_type']['id']
        event_type = EventType.objects.get(id=event_type)
        validated_data['event_type'] = event_type
        event = Event.objects.create(**validated_data)
        event.save()
        return event

    def update(self, instance, validated_data):
        print(validated_data)
        event_type = validated_data['event_type']['id']
        event_type = EventType.objects.get(id=event_type)
        validated_data['event_type'] = event_type
        # if attr in info.relations and info.relations[attr].to_many:
        #         m2m_fields.append((attr, value))
        #     else:
        #         setattr(instance, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # event = instance.update(**validated_data)
        instance.save()
        return instance

    #     return worker

    # def to_representation(self, instance):


class HeadEventSerializer(serializers.ModelSerializer):
    """_summary_
        Создание событий для подчиненных
    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    company_data = CompanySerializer(required=True)

    class Meta:
        model = Worker
        read_only_fields = (
            "user_id",
            "created_at",
            "head",
            "company",
        ),
        fields = "__all__"

    def create(self, validated_data):
        company_data = validated_data.pop('company_data')
        worker = Worker.object.create(**validated_data)
        worker.save()
        company = Company.object.create(**company_data)
        company.created_by = worker.id
        company.head = worker.id
        company.save()
        worker.company = company.id
        worker.save()
        return worker
