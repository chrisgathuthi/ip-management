import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import CustomerInfoSerializer, ReadIpAddressSerializer, WriteIpAddressSerializer, CustomerSerializer
from .models import IpAddress, CustomerInfo
# Create your views here.

class AllocateIP(APIView):

    """allocating ip view"""
    # authentication_classes = [TokenAuthentication]

    #>> MOVE THE GET TO A NEW VIEWSET CLASS. FROM THE NOTES THIS SHOULD ONLY BE A POST ROUTE
    # def get(self, request, *args, **kwargs):
    #     qs = IpAddress.objects.filter(status="allocated")
    #     serializer = ReadIpAddressSerializer(qs, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        ip = IpAddress.objects.filter(status="available").first() #>> NO NEED FOR DISTINCT
        is_allocated = CustomerInfo.objects.filter(ip_address=ip).exists()
 
        if not ip or is_allocated:
            raise serializers.ValidationError("No ip address available", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #print(request.data)
        data = request.data #| {"ip_address": ip.id} #>> I AM NOT SURE WHAT YOU WERE ATTEMPTING HERE
        #print(data)
        # serializer = CustomerInfoSerializer(data=data) #>> I USED A NEW SERIALIZER HERE
        
        # ip = ReadIpAddressSerializer(ip) #>> I DON'T THINK THIS IS NEEDED HERE NOW
        if serializer.is_valid(raise_exception=True):
            #print(serializer.validated_data)
            #>> INSTEAD OF SAVING THE SERIALIZER OBJECT, I CHOSE TO CREATE A NEW OBJECT. EVERYTHING SHOULD BE GOOD AS THE DATA IS ALREADY VALIDATED BY THE SERIALIZER ABOVE. THE REASON FOR THIS APPROACH IS TO SAVE THE ID OF THE IP ADDRESS OBJECT DIRECTLY TO THE DATABASE. I SEE THE IP ADDRESS STATUS IS ADDRESS BY THE SIGNAL YOU CREATED.
            customer = CustomerInfo.objects.create(customer_name=serializer.data.get('customer_name'), email=serializer.data.get('email'), ip_address=ip)
            #>> SERIALIZER TAKES CARE OF FETCHING THE IP ADDRESS TO RETURN HERE
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
            # serializer.save()
            # return Response(data=ip.data,status=status.HTTP_201_CREATED)
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
        