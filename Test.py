import pyfiglet
import time
from datetime import datetime
import socket
import multiprocess

def main():
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    print("-" * 50)

    print("Getting host details: ")
    socket.gethostbyname(socket.gethostname())
    h_ip = socket.gethostbyname(socket.gethostname())
    print(f"Host IP: {h_ip}")

    print("-" * 50)
    print("Scanning Target: " + h_ip)
    print("Scanning started at: " + str(datetime.now()))
    print("-" * 50)

    max_max = 65535

    with open("Session_File.txt", "w"):
        pass



    def hyper_thread(min, max):
        for port in range(min, max):
            time.sleep(1)
            print(port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            
            
            # returns an error indicator
            result = s.connect_ex((h_ip, port))
            if result ==0:
                print(f"Port {port} is open")
                with open("Session_File.txt", "a") as file:
                    file.write(f"Port number: {port} is open \n")
                
            s.close()

    process = []
    for _ in range(85):
        
        min = _*771 + 1
        max = min + 772

        p = multiprocess.Process(target=hyper_thread, args=(min, max))
        p.start()
        process.append(p)

    for proces in process:
        proces.join()

    
    
if __name__ == '__main__':
    main()
