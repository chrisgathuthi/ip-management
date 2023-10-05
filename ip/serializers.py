from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import IpAddress, CustomerInfo


class UserSerializer(serializers.ModelSerializer):
    
    """serialize user model"""

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "first_name", "last_name","password"]
    
    def create(self, validated_data):
        User= get_user_model()
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class WriteIpAddressSerializer(serializers.ModelSerializer):

    """serialize Ip address only"""
    class Meta:
        model = IpAddress
        fields = ("address",)

class ReadIpAddressSerializer(serializers.ModelSerializer):

    """ip address serailizer with customerinfo"""

    customer_name = serializers.CharField(source='ip.customer_name')
    email = serializers.EmailField(source='ip.email')

    class Meta:
        model = IpAddress
        fields = ["status", "address", "customer_name", "email"]
    
    def update(self, instance, validated_data):
        
        if IpAddress.objects.filter(address=validated_data["address"], status="allocated").exists():
            raise serializers.ValidationError(detail={"The ip address already allocated"}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            instance.address = validated_data.get('address', instance.address)
            instance.status = validated_data.get('status', instance.status)
            instance.save()
            return instance

class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpAddress
        fields = ['address', 'status']


class CustomerSerializer(serializers.ModelSerializer):
    ip_address = serializers.StringRelatedField() 
    class Meta:
        model = CustomerInfo
        fields = ['customer_name', 'email', 'ip_address']

