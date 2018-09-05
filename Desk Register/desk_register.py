from config_server import *
from time import sleep
from subprocess import call

import requests, sys
import socket
import fcntl
import struct
import re

class DeskRegister :
    def __init__(self, ip_address_server, url_post_data, timeout_conn) :
        self.ip_address_server = ip_address_server
        self.url_post_data = url_post_data
        self.timeout_conn = timeout_conn # seconds
        
    def register(self, barcode) :
        try :
            param = {"barcode" : barcode, "ipv4" : self.get_ip_address()}
            url = self.ip_address_server + self.url_post_data
            response = requests.post(url, data=param, timeout=self.timeout_conn)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            if data_json['status'] == 204 :
                self.play_sound("success")
            else :
                self.play_sound("error")
        except requests.exceptions.ConnectionError as errc :
            self.play_sound("error")
            print("Error : cannot establish connection to server. Please configure the server properly.")
            self.retry_connect()
            self.reconnect(barcode)
        except requests.exceptions.Timeout as errt :
            self.play_sound("error")
            print(errt)
            self.retry_connect()
            self.reconnect(barcode)
        except requests.exceptions.HTTPError as errh :
            self.play_sound("error")
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
        if self.ip_address_server != "" and self.url_post_data != "" :
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
        self.register(barcode)
        
    def play_sound(self, type) :
        if type == "error" :
            file_name = "beep-error.wav"
        else :
            file_name = "beep-success.wav"
        file_path = dir_path_sound + file_name
        call(['aplay', file_path])
            
    def main(self) :
        while True :
            barcode = str(input("Scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode).replace("B", "")
            if barcode != "" :
                self.register(barcode)
            else :
                print("Invalid Barcode")
            print("\n")