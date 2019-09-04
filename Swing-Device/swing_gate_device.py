from config import *
from time import sleep
from subprocess import call

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
<<<<<<< HEAD
            par = {"barcode" : barcode, "ipv4" : self.get_ip_address("wlan0")}
            print(par)
=======
            par = {'barcode' : barcode, 'ipv4' : self.get_ip_address()}
>>>>>>> 668357933884cccd7155ce598989e491c34bba20
            url = ip_address_server + url_check_ticket
            print(url)
            response = requests.post(url, json=par, timeout=timeout_connection)
            print("response = " + str(response))
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            if data_json['status'] == 200 :
                self.relay.on()
                sleep(delay_time)
                self.play_sound(path_sound_file_success)
            else :
                self.play_sound(path_sound_file_invalid)
            self.relay.off()
        except requests.exceptions.ConnectionError as errc :
            self.play_sound(path_sound_file_error_conn)
            print("cannot establish connection to server. please setup the server properly.")
            self.retry_connect()
            self.main()
        except requests.exceptions.Timeout as errt:
            self.play_sound(path_sound_file_error_timeout)
            print(errt)
            self.retry_connect()
            self.main()
        except requests.exceptions.HTTPError as err :
            self.play_sound(path_sound_file_error_http)
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
    
    def play_sound(self, path_sound_file) :            
        call(['aplay', path_sound_file])
        
    def main(self) :
        while True :
            barcode = str(input("scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode)
            print("input = " + str(input_barcode))
            if barcode != "" :
                self.check_ticket_validity(input_barcode)
            else :
                print("Invalid Barcode")
                self.play_sound(path_sound_file_invalid)
            print("\n")
