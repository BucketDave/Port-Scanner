import time
from datetime import datetime
import socket
import ipaddress
import os
from colorama import Fore, Back, Style
import subprocess
import win32evtlog
import win32evtlogutil

# Getting current working environment directory
cwd = os.getcwd()

# Getting User-input
def UserInput():
    # Identify the range of computers to be check
        # Retriving Subnet prefix & mask
    print("-"*50)
    sub_pre = input("Enter IPv4 subnet prefix: ")
    sub_pre_mask = input(f"Enter subnet mask of [{sub_pre}]: ")
    print("-"*50)
    # Displaying details to user
    print(f"Verifying details."
        f"\nSubnet prefix: {sub_pre}"
        f"\nSubnet mask: {sub_pre_mask}")
    print("-"*50)
    return sub_pre, sub_pre_mask

# Verifying User-input
def Verification(sub_pre, sub_pre_mask):
    # Verifying user input
    try:
        if "/" in sub_pre_mask:
            validate = ipaddress.IPv4Network(f"{sub_pre}{sub_pre_mask}", strict=False)
            print(f"Network IP: {validate}")
            print(f"Network Range: {validate.network_address} - {validate.broadcast_address}\n")
            return validate
        else:
            # Checking if input is valid
            validate = ipaddress.IPv4Network(f"{sub_pre}/{sub_pre_mask}", strict=False)
            print(f"Network IP: {validate}")
            print(f"Network Range: {validate.network_address} - {validate.broadcast_address}\n")
            return validate
    except:
        # Invalid input
        print(f"User entered details of"
              f"\nSubnet prefix: {sub_pre}"
              f"\nSubnet mask: {sub_pre_mask}"
              "\nAre Invalid"
              "\nPlease enter valid details")
        time.sleep(2)
        return False

#Displaying contents of 'Verification'
def Displaying(validate):
    # Printing hosts meeting requirements
        # Displaying criteria
    print("Generating host IPs in range of user selected network"
        "\nRequirements:"
        "\n [1] -- Skipping the last 10 host address"
        "\n [2] -- Skipping every EVEN IP")
    print("-"*50)
        # Getting all hosts 
    hostlist = list(validate.hosts())
    print(f"All Possible IPs: [{len(hostlist)}]")
    print("-"*50)
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
        print(f"Scanning all [{len(sorted_hostlist)}] IPs")
    return sorted_hostlist

# Reading ports from ports.txt file
def ReadingFile():
    ports = []
    try:
        with open("ports.txt","r") as port_file:
            port_file = port_file.read().splitlines()
            for i in port_file:
                try:
                    i = int(i)
                    if 0 < i < 65535:
                        ports.append(i)
                except:
                    print(f"[{i}] is not a 'int'"
                          f"\nPassing")
        return ports
    except Exception as e:
        txt_dir = os.path.join(cwd, "ports.txt")
        if not os.path.exists(txt_dir):
            print(f"ports.txt file cannot be found in [{cwd}]")
            print(f"Terminating program")
            quit()
        else:
            print(e)

# IP address that are unavailable for port scanning are to be noted as "unavailable" 
# Checks if ip is 'ping'able
def IsAlive(ip):
    result = subprocess.run(['ping', "-n", '2', "-w", "500", ip], capture_output=True)
    if result.returncode == 0:
        return True
    else:
        return False

# Getting hostname from ip if 'Alive'
def IP_Hostname(ip):
    result = subprocess.run(["tracert", ip], capture_output=True)
    result = str(result.stdout)
    result = ((result.split("\\n", 1))[1])
    result = ((result.split("to ", 1))[1])
    result = ((result.split(" [", 1))[0])
    return result

# Scan Ports
# Output the status of each port including "port open" or "port closed"
def Scanning(ip: str, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    
    result = s.connect_ex((ip, port))
    if result == 0:
        print(Fore.GREEN + f"Port {port} is OPEN" + Style.RESET_ALL)

        
    else:
        print(f"Port {port} is CLOSED")
    s.close()

def EventLogging(ip_address):
    DUMMY_EVT_APP_NAME = "Gelos Port Scanner"
    DUMMY_EVT_ID = 0 
    DUMMY_EVT_CATEG = 1
    DUMMY_EVT_STRS = [f"{ip_address}"]
    DUMMY_EVT_DATA = b"Dummy event data"


    win32evtlogutil.ReportEvent(
        DUMMY_EVT_APP_NAME,
        DUMMY_EVT_ID,
        eventCategory=DUMMY_EVT_CATEG,
        eventType=win32evtlog.EVENTLOG_WARNING_TYPE, strings=DUMMY_EVT_STRS,
        data=DUMMY_EVT_DATA)


def Boot():
    while True:
        sub_pre, sub_pre_mask = UserInput()
        validate = Verification(sub_pre, sub_pre_mask)
        
        if validate:
            break
    
    host_list = Displaying(validate)
    ports = ReadingFile()

    for ip in host_list:
        isalive = IsAlive(str(ip))
        if isalive:
            EventLogging(str(ip))
            hostname = IP_Hostname(str(ip))
            print("-"*50)
            print(f"Scanning IP [{ip}] Hostname: {hostname}")
            for port in ports:
                print("-"*25)
                print(f"Scanning Port [{port}]")
                Scanning(str(ip), port)
            print("-"*50)
        else:
            print(f"[{ip}] Unavailable")

if __name__ == "__main__":
    Boot()

