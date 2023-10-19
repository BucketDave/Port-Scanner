import time
from datetime import datetime
import socket
import threading
import ipaddress

# Identify the range of computers to be check
    # Retriving Subnet prefix & mask
while True:
    print("-"*50)
    sub_pre = input("Enter IPv4 subnet prefix: ")
    sub_pre_mask = input(f"Enter subnet mask of [{sub_pre}]: ")
    print("-"*50)
    # Displaying details to user
    print(f"Verifying details."
        f"\nSubnet prefix: {sub_pre}"
        f"\nSubnet mask: {sub_pre_mask}")
    print("-"*50)
    # Verifying user input
    try:
        if "/" in sub_pre_mask:
            validate = ipaddress.IPv4Network(f"{sub_pre}{sub_pre_mask}", strict=False)
            print(f"Network IP: {validate}")
            print(f"Network Range: {validate.network_address} - {validate.broadcast_address}\n")
            break
        else:
            # Checking if input is valid
            validate = ipaddress.IPv4Network(f"{sub_pre}/{sub_pre_mask}", strict=False)
            print(f"Network IP: {validate}")
            print(f"Network Range: {validate.network_address} - {validate.broadcast_address}\n")
            break
    except:
        # Invalid input
        print(f"User entered details of"
              f"\nSubnet prefix: {sub_pre}"
              f"\nSubnet mask: {sub_pre_mask}"
              "\nAre Invalid"
              "\nPlease enter valid details")
        time.sleep(2)
# Printing hosts meeting requirements
    # Displaying criteria
print("Generating host IPs in range of user selected network"
      "\nRequirements:"
      "\n [1] -- Skipping the last 10 host address"
      "\n [2] -- Skipping every EVEN IP")
print("-"*50)
    # Getting all hosts 
hostlist = list(validate.hosts())
    # Removing last 10 hosts
if len(hostlist) <= 10:
    print(f"Number of host IPs [{len(hostlist)}] is less then or equal to 10"
          "\nCannot carry out requirement [1]"
          "\nTerminating Program")
    print("-"*50)
    time.sleep(1)
else:
    for ip in range(10):
        hostlist.pop(-1)
        # New List to hold sorted hosts
    sorted_hostlist = []
        # Sorting host by the value of the last octect
    for num in hostlist:
        str_num = str(num)
        last_octect = int(str_num.split(".", 3)[3])
        # Checking if last octect value is divisible by 2
        devide = last_octect % 2
        if devide == 1:
            sorted_hostlist.append(num)
    # Print sorted list
    print(f"Number of available IPs: [{len(sorted_hostlist)}]")
    print(f"Listing all [{len(sorted_hostlist)}] IPs")
    print("-"*50)
    for i in sorted_hostlist:
        print(i)

# Scan Ports

# Output the status of each port including "port open" or "port closed" \

# IP address that are unavailable for port scanning are to be noted as "unavailable" 




