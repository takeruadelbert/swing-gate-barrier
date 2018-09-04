from server_config import ip_address_server, url_check_ticket
import requests, sys
import socket
import fcntl
import struct
import gpiozero
from time import sleep
import re

class SwingGate :
    def __init__(self, ip_address_server, url_check_ticket) :
        self.ip_address_server = ip_address_server
        self.url_check_ticket = url_check_ticket
        self.relay_pin = 2
        self.relay = gpiozero.OutputDevice(self.relay_pin, active_high=False, initial_value=False, pin_factory=None)
        self.delay_time = 0.5 # half second
        
    def check_ticket_validity(self, barcode) :
        try :
            par = {'barcode' : barcode, 'ipv4' : self.get_ip_address()}
            url = self.ip_address_server + self.url_check_ticket
            response = requests.get(url, params=par, timeout=10)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            if data_json['status'] == 206 or data_json['status'] == 200 :
                self.relay.on()
                sleep(self.delay_time)
            self.relay.off()
        except requests.exceptions.ConnectionError as errc :
            print("cannot establish connection to server. please setup the server properly.")
            sys.exit(1)
        except requets.exceptions.Timeout as errt:
            print(errt)
            sys.exit(1)
        except requests.exceptions.HTTPError as err :            
            print(err)
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
            barcode = str(input("scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode).replace("B", "")
            if barcode != "" :
                self.check_ticket_validity(input_barcode)
            else :
                print("Invalid Barcode")
            print("\n")

if __name__ == "__main__" :
    swing = SwingGate(ip_address_server, url_check_ticket)
    swing.main()