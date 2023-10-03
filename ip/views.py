import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import CustomerInfoSerializer, ReadIpAddressSerializer, WriteIpAddressSerializer
from .models import IpAddress, CustomerInfo
# Create your views here.

class AllocateIP(APIView):

    """allocating ip view"""
    # authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        qs = IpAddress.objects.filter(status="allocated")
        serializer = ReadIpAddressSerializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        ip = IpAddress.objects.filter(status="available").distinct().first()
        is_allocated = CustomerInfo.objects.filter(ip_address=ip).exists()
 
        if not ip or is_allocated:
            raise serializers.ValidationError("No ip address available", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        print(request.data)
        data = request.data | {"ip_address": ip.id}
        print(data)
        serializer = CustomerInfoSerializer(data=data)

        ip = ReadIpAddressSerializer(ip)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            serializer.save()
            return Response(data=ip.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListAvailableIP(APIView):

    """list available IPs"""

    def get(self, request, format=None):
        queryset = IpAddress.objects.filter(status='available')
        serializer = ReadIpAddressSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateIp(APIView):

    """change ip status"""

    def get(self, request, *args, format=None, **kwargs):

        queryset = IpAddress.objects.filter(address=kwargs['address'])

        if not queryset:
            return Response(data={"ip address does not exist"},status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ReadIpAddressSerializer(queryset, many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, *args, format=None, **kwargs):
        serializer = ReadIpAddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CustomerInfoViewset(APIView):

    def get(self, request, *args, format=None, **kwargs):
        queryset = CustomerInfo.objects.get(id=kwargs["pk"])
        serializer = CustomerInfoSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        