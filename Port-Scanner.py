import pyfiglet
import time
from datetime import datetime
import socket
import multiprocess
from colorama import Fore, Back, Style

def main():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    print("-" * 50)

    print("Getting host details: ")
    h_ip = socket.gethostbyname(socket.gethostname())
    print(f"Host IP: {h_ip}")
    print("-" * 50)
    print("Press 'N' to terminate program.")
    print("Press 'M' to enter manually")
    print("Press 'Y' to proceed.")

    loop = True
    while loop:
        confirm = input("-"*18 + "Confirm[Y/N/M]" + "-"*18 + "\n:")
        confirm = confirm.lower()

        if confirm == "y":
            break
        elif confirm == "n":
            print("Terminating Program")
            time.sleep(1)
            quit()
        elif confirm == "m":
            looploop = True
            newip = input("Enter local target ip: \n:")

            while looploop:
                confirm = input(f"Target Confirm[Y/N]: Target= {newip}" "\n:")
                confirm = confirm.lower()
                if confirm == "y":
                    h_ip = newip
                    break
                elif confirm == "n":
                    print("Terminating Program")
                    time.sleep(1)
                    quit()
                else:
                    print("Enter a valid letter")
            break


        else:
            print("Enter a valid letter")

    print("-" * 50)
    print("Scanning Target: " + h_ip)
    print("Scanning started at: " + str(datetime.now()))
    print("-" * 50)
    
    max_max = 65535

    with open("Session_File.txt", "w"):
        pass
    time.sleep(2)

    def hyper_thread(min, max):
        for port in range(min, max):
            print(Fore.YELLOW + f"Trying port {port}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            result = s.connect_ex((h_ip, port))
            if result == 0:
                print(Fore.GREEN + f"Port {port} is OPEN")
                with open("Session_File.txt", "a") as file:
                    file.write(f"Port number: [{port}] is open \n")
            else:
                print(Fore.RED + f"Port {port} is CLOSED")
            s.close()

    process = []
    for _ in range(255):
        
        min = _*257 + 1
        max = min + 256 + 1

        p = multiprocess.Process(target=hyper_thread, args=(min, max))
        p.start()
        process.append(p)

    for proces in process:
        proces.join()

    print(Fore.GREEN + "Done")
    print(Style.RESET_ALL)


if __name__ == '__main__':
    main()
