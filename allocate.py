from ip.models import IpAddress, CustomerInfo


for i in range(10):
    ip = f"192.168.1.1{i}"

    status = [
        "reserved",
        "allocated",
        "available"
    ]
    print(ip)
    IpAddress.objects.create(address=ip,status=choice(status))
