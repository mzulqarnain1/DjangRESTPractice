"""
This module contains serializers for all the models classes
in our api application.
"""
from rest_framework import serializers
from api.models import Property, PropertyType, Status
from django.contrib.auth.models import User


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer for our Property model.
    """
    class Meta:
        model = Property
        fields = ('id', 'address', 'owner', 'status', 'type', 'parentProperty')

    owner = serializers.ReadOnlyField(source='owner.username')


class PropertyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyType
        fields = ('id', 'name', 'description')


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'name', 'description')


class UserSerializer(serializers.ModelSerializer):

    properties = serializers.HyperlinkedRelatedField(
        many=True, queryset=Property.objects.all(),
        view_name='property-details')

    class Meta:
        model = User
        fields = ('id', 'username', 'properties')
