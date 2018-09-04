from config_server import ip_address_server, url
import requests, sys
import socket
import fcntl
import struct
import re

class DeskRegister :
    def __init__(self, ip_address_server, url_post_data) :
        self.ip_address_server = ip_address_server
        self.url_post_data = url_post_data
        
    def register(self, barcode) :
        try :
            param = {"barcode" : barcode, "ipv4" : self.get_ip_address()}
            url = self.ip_address_server + self.url_post_data
            response = requests.post(url, data=param, timeout=10)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
        except requests.exceptions.ConnectionError as errc :
            print("Error : cannot establish connection to server. Please configure the server properly.")
            sys.exit(1)
        except requests.exceptions.Timeout as errt :
            print(errt)
            sys.exit(1)
        except requests.exceptions.HTTPError as errh :
            print(errh)
            sys.exit(1)
    
    def get_ip_address(self, ifname = 'eth0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        return str(ip_address)
            
    def main(self) :
        while True :
            barcode = str(input("Scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode).replace("B", "")
            if barcode != "" :
                self.register(barcode)
            else :
                print("Invalid Barcode")
            print("\n")

if __name__ == "__main__" :
    desk = DeskRegister(ip_address_server, url)
    desk.main()