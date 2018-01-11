
from rest_framework import serializers
from api.models import Property, PropertyType, Owner, Status


class PropertySerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Property
        fields = ('id', 'address', 'owner', 'status', 'type', 'parentProperty')


class PropertyTypeSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = PropertyType
        fields = ('id', 'name', 'description')


class StatusSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Status
        fields = ('id', 'name', 'description')


class OwnerSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Owner
        fields = ('id', 'cnic', 'name', 'gender')
