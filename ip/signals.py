from .models import CustomerInfo, IpAddress
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomerInfo)
def change_ip_status(sender, created, instance, *args, **kwargs):

    """change ip status"""

    if created:
        print(instance)
        print(instance.__dict__)
        instance_ip = IpAddress.objects.get(id = instance.ip_address.id)
        instance_ip.status = "allocated"
        print(instance_ip.status)
        instance_ip.save()
