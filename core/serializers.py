from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Event, Tag, Fest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username','first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
                    'first_name': {'required': True},
                    'last_name_name': {'required': True},
                    'email': {'required': True, 'validators': [UniqueValidator(queryset=User.objects.all())]},
                    'password': {'write_only': True}
                    } 

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    is_admin = serializers.CharField(source='is_staff')
    class Meta:
        model = User
        fields = ('id', 'username','first_name', 'last_name', 'email', 'is_admin')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
        )


class EventSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(source='get_tags')
    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'link',
            'date',
            'timezone',
            'description',
            'tags',
            'image',
            'status',
            'archived',
            'updated_at',
        )

    def get_tags(self, obj):
        return TagSerializer(obj.tags.filter(archived=False), many=True, read_only=True).data

class EventEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'link',
            'date',
            'timezone',
            'description',
            'tags',
            'image',
        )

class FestOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fest
        fields = (
            'id',
            'cover',
            'name',
            'date_start',
            'date_end',
            'timezone',
        )


class FestDetailsSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField(source='get_events')
    class Meta:
        model = Fest
        fields = (
            'id',
            'name',
            'cover',
            'description',
            'date_start',
            'date_end',
            'timezone',
            'events',
        )

    def get_events(self, obj):
        return EventSerializer(obj.events.filter(archived=False, status="A"), many=True, read_only=False).data


class FestEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fest
        fields = (
            'id',
            'name',
            'cover',
            'description',
            'date_start',
            'date_end',
            'timezone',
            'events',
        )