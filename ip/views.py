import json
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import ReadIpAddressSerializer, IpSerializer, CustomerSerializer, WriteIpAddressSerializer, UserSerializer
from .models import IpAddress, CustomerInfo
from .subnet_calculator import calculate_subnet_details
# Create your views here.


class AllocateIP(APIView):

    """allocating ip address to customer"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def post(self, request, format=None):

        ip = IpAddress.objects.filter(status="available").first()
        is_allocated = CustomerInfo.objects.filter(ip_address=ip).exists()

        if not ip or is_allocated:
            raise serializers.ValidationError(
                "No ip address available", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            customer = CustomerInfo.objects.create(customer_name=serializer.data.get(
                'customer_name'), email=serializer.data.get('email'), ip_address=ip)
            ip = WriteIpAddressSerializer(ip)
            return Response(data=ip.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllocatedIpView(APIView):

    """allocated IP with customer informatin"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(request=None, responses=ReadIpAddressSerializer)
    def get(self, request, *args, **kwargs):

        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if start and end:
            queryset = IpAddress.objects.filter(status='allocated').filter(
                address__range=(start, end)
            )
        else:
            queryset = IpAddress.objects.filter(status='allocated')

        qs = IpAddress.objects.filter(status="allocated")
        serializer = ReadIpAddressSerializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListAvailableIP(APIView):

    """list available IPs"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReadIpAddressSerializer  # swagger documentation

    def get(self, request, format=None):
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if start and end:
            queryset = IpAddress.objects.filter(status='available').filter(
                address__range=(start, end)
            )
        else:
            queryset = IpAddress.objects.filter(status='available')
        serializer = IpSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateIp(APIView):

    """change ip status, release"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, format=None, **kwargs):

        queryset = IpAddress.objects.filter(address=kwargs['address'])

        if not queryset:
            return Response(data={"ip address does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = IpSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, format=None, **kwargs):
        serializer = IpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SubnetCalculator(APIView):

    """Ip subnet calculator"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    #swagger documentation
    @extend_schema(description="subnet calculator",
                   parameters=[
                       OpenApiParameter(name="ip address",
                                        type=str,
                                        required=True,
                                        location=OpenApiParameter.QUERY,
                                        description="ip address"),

                       OpenApiParameter(name="subnet mask",
                                        type=str,
                                        required=True,
                                        location=OpenApiParameter.QUERY,
                                        description="subnet mask")
                   ])
    def get(self, request, format=None):
        ip_address = request.query_params.get("ip_address")
        subnet_musk = request.query_params.get("subnet_mask")

        results = calculate_subnet_details(
            ip_str=ip_address, subnet_mask_str=subnet_musk)
        return Response(data=results, status=status.HTTP_200_OK)


class Registrationviewset(APIView):

    """user registration"""
    serializer_class = UserSerializer  # swagger documentation

    def get(self, request, format=None):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
