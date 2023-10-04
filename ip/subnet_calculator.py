import ipaddress
from typing import Dict

def calculate_subnet_details(ip_str: str, subnet_mask_str:str) ->Dict[str, str]:
    try:
        # Parse the IP address and subnet mask
        ip = ipaddress.IPv4Address(ip_str)
        subnet_mask = ipaddress.IPv4Address(subnet_mask_str)

        # Calculate the network address and broadcast address
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        network_address = network.network_address
        broadcast_address = network.broadcast_address

        # Calculate the usable IP range (exclude network and broadcast addresses)
        usable_ip_range = list(network.hosts())
        
        return {
            "IP Address": str(ip),
            "Subnet Mask": str(subnet_mask),
            "Network Address": str(network_address),
            "Broadcast Address": str(broadcast_address),
            "Usable IP Range": [str(ip) for ip in usable_ip_range[:10]],
        }
    except ValueError as e:
        return {"error": str(e)}

# if __name__ == "__main__":
#     # Input IP address and subnet mask
#     ip_address = input("Enter IP Address: ")
#     subnet_mask = input("Enter Subnet Mask: ")

#     # Calculate subnet details
#     result = calculate_subnet_details(ip_address, subnet_mask)
#     print(result)
#     # Display the results
#     if "error" in result:
#         print("Error:", result["error"])
#     else:
#         print("\nSubnet Details:")
#         for key, value in result.items():
#             print(f"{key}: {value}")
