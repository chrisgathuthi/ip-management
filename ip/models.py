from django.db import models

# Create your models here.

class IpAddress(models.Model):

    """IP address model"""

    class STATUS(models.TextChoices):
        reserved = "reserved"
        allocated = "allocated"
        available = "available"
    address = models.GenericIPAddressField(verbose_name="ip address", unique=True)
    status = models.CharField(max_length=9,choices=STATUS.choices)

    def __str__(self):
        return self.address

class CustomerInfo(models.Model):

    """customer information model"""

    ip_address = models.OneToOneField(IpAddress, on_delete=models.SET_NULL, null=True, related_name="ip")
    customer_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.customer_name


