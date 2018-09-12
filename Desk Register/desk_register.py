from config import *
from time import sleep
from subprocess import call

import requests, sys
import socket
import fcntl
import struct
import re

class DeskRegister :        
    def register(self, barcode) :
        try :
            param = {"barcode" : barcode, "ipv4" : self.get_ip_address()}
            full_url = ip_address_server + url
            response = requests.post(full_url, data=param, timeout=timeout_connection)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            if data_json['status'] == 204 :
                self.play_sound(path_sound_file_success)
            else :
                self.play_sound(path_sound_file_invalid)
        except requests.exceptions.ConnectionError as errc :
            self.play_sound(path_sound_file_error_conn)
            print("Error : cannot establish connection to server. Please configure the server properly.")
            self.retry_connect()
            self.reconnect(barcode)
        except requests.exceptions.Timeout as errt :
            self.play_sound(path_sound_file_error_timeout)
            print(errt)
            self.retry_connect()
            self.reconnect(barcode)
        except requests.exceptions.HTTPError as errh :
            self.play_sound(path_sound_file_error_http)
            print(errh)
            self.retry_connect()
            self.reconnect(barcode)            
    
    def get_ip_address(self, ifname = 'eth0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        return str(ip_address)
    
    def check_server_config(self) :
        if ip_address_server != "" and url != "" :
            return True
        else :
            return False
        
    def retry_connect(self) :
        x = reconnect_time # seconds
        while x >= 1 :
            print("Retrying connect to server in " + str(x) + " second ...")
            sleep(1)
            x = x - 1
        print("Connecting ...")
    
    def reconnect(self, barcode) :
        self.main()
        
    def play_sound(self, path_file_sound) :
        call(['aplay', path_file_sound])
            
    def main(self) :
        while True :
            barcode = str(input("Scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode).replace("B", "")
            if barcode != "" :
                self.register(input_barcode)
            else :
                self.play_sound(path_sound_file_invalid)
                print("Invalid Barcode")
            print("\n")