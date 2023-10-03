from rest_framework import serializers
from rest_framework import status
from .models import IpAddress, CustomerInfo


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

class CustomerInfoSerializer(serializers.ModelSerializer):

    """customer information serializer"""
    ip_address = ReadIpAddressSerializer(read_only=True)
    class Meta:
        model = CustomerInfo
        fields = ["ip_address", "customer_name", "email"]
        depth = 2
        

