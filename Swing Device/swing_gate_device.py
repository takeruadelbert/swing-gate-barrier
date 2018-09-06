from config import *
from time import sleep

import requests, sys
import socket
import fcntl
import struct
import gpiozero
import re

class SwingGate :
    def __init__(self) :
        self.relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False, pin_factory=None)
        
    def check_ticket_validity(self, barcode) :
        try :
            par = {'barcode' : barcode, 'ipv4' : self.get_ip_address()}
            url = ip_address_server + url_check_ticket
            response = requests.get(url, params=par, timeout=timeout_connection)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            if data_json['status'] == 206 or data_json['status'] == 200 :
                self.relay.on()
                sleep(delay_time)
            self.relay.off()
        except requests.exceptions.ConnectionError as errc :
            print("cannot establish connection to server. please setup the server properly.")
            self.retry_connect()
            self.main()
        except requets.exceptions.Timeout as errt:
            print(errt)
            self.retry_connect()
            self.main()
        except requests.exceptions.HTTPError as err :            
            print(err)
            self.retry_connect()
            self.main()
            
    def get_ip_address(self, ifname = 'eth0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        return str(ip_address)
    
    def retry_connect(self) :
        x = retry_connect
        while(x >= 1) :
            print("Retrying connect to server in " + str(x) + " second ...")
            sleep(1)
            x -= 1
        print("Reconnecting ...")
        
    def main(self) :
        while True :
            barcode = str(input("scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode).replace("B", "")
            if barcode != "" :
                self.check_ticket_validity(input_barcode)
            else :
                print("Invalid Barcode")
            print("\n")