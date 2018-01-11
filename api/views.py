from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Property, PropertyType, Status
from api.serializers import PropertySerializer, PropertyTypeSerializer,  StatusSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def property_list(request):
    """
    List all code Property, or create a new Property.
    """
    if request.method == 'GET':
        propertys = Property.objects.all()
        serializer = PropertySerializer(propertys, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT'])
def property_detail(request, pk):
    """
    :param request:
    :return:
    """
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'POST'])
def status_list(request):
    """
    List all code Status, or create a new Status.
    """
    if request.method == 'GET':
        property_status = Status.objects.all()
        serializer = StatusSerializer(property_status, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT'])
def status_detail(request, pk):
    """
    :param request:
    :return:
    """
    try:
        property_status = Status.objects.get(pk=pk)
    except Status.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StatusSerializer(property_status)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        property_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = StatusSerializer(property_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyTypeList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request):
        types = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertyTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyTypeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return PropertyType.objects.get(pk=pk)
        except PropertyType.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PropertyTypeSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PropertyTypeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
