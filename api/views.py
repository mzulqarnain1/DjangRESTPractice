from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from api.models import Property, PropertyType, Status
from api.permissions import IsOwnerOrReadOnly, IsSelf
from api.serializers import (PropertySerializer, PropertyTypeSerializer,
                             StatusSerializer, UserSerializer)


class PropertyList(generics.ListCreateAPIView):
    """
    This view handles request for returning a list of properties
    or creating a new property.
    """
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint handles retrieval, updation and deletion
    of specific property object.
    """
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrReadOnly,)
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class StatusList(generics.ListAPIView):
    """
    This view handles request for returning a list of statuses
    or creating a new status.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusDetail(generics.RetrieveAPIView):
    """
    This endpoint handles retrieval, updation and deletion
    of specific status object.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class PropertyTypeList(generics.ListAPIView):
    """
    This view handles request for returning a list of types
    or creating a new type.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class PropertyTypeDetail(generics.RetrieveAPIView):
    """
    This endpoint handles retrieval, updation and deletion
    of specific property type object.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class UserList(generics.ListAPIView):
    """
    This view handles request for returning a list of users.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This endpoint handles retrieval, updation and deletion
    of specific user object if and only if it is user's own
    profile.
    """
    permission_classes = (permissions.IsAuthenticated,
                          IsSelf)
    queryset = User.objects.all()
    serializer_class = UserSerializer
