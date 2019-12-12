from config import *
from time import sleep
from subprocess import call

import requests, sys, os
import socket
import fcntl
import struct
import gpiozero
import re
import datetime
import asyncio

class SwingGate :
    def __init__(self) :
        self.relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False, pin_factory=None)
        self.message = ""
        
    def request_api(self, barcode, url, payload):
        hasError = False
        try:
            self.writeLog("Checking '" + barcode + "' ...")
            response = requests.post(url, json=payload, timeout=timeout_connection, verify=False)
            response.raise_for_status()
            data_json = response.json()
            print(data_json)
            self.message = data_json['message']
            self.writeLog("Getting Response from " + url + " ...")
            if data_json['status'] == 200:
                self.relay.on()
                self.play_sound(path_sound_file_success)
                sleep(delay_time)                
                self.writeLog(self.message)
                self.relay.off()
                return 200
            elif data_json['status'] == 401:
                self.writeLog(self.message)
                return 401
            else:
                self.writeLog(data_json['message'])
                return data_json['status']
        except requests.exceptions.ConnectionError as errc :
            self.message = "cannot establish connection to " + url + ". please setup the server properly."
            self.writeLog(self.message)
            return 408 # connection timeout
        except requests.exceptions.Timeout as errt:
            hasError = True
            self.message = str(errt)
        except requests.exceptions.HTTPError as err :
            hasError = True
            self.message = str(err)
        except Exception as ex:
            hasError = True
            self.message = str(ex)
        finally:
            if hasError:
                self.writeLog(self.message)
                return 500 # indicates error
        
    def check_ticket_validity(self, barcode) :
        try:
            payload = {"barcode" : barcode, "ipv4" : self.get_ip_address()}
            url1 = ip_address_server + url_check_ticket
            url2 = ip_address_server2 + url_check_ticket
            response1 = self.request_api(barcode, url1, payload)
            if response1 == 401 or response1 == 408:
                response2 = self.request_api(barcode, url2, payload)
                if response2 == 500:
                    self.retry_connect()
                    self.main()
            elif response1 == 500:
                self.retry_connect()
                self.main()
        except Exception as ex:
            errorMessage = str(ex)
            self.writeLog(errorMessage)
            self.play_sound(path_sound_file_error_conn)
            
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
        if set_to_play:
            call(['aplay', path_sound_file])
        
    def writeLog(self, message):
        try:
            print(message)
            filename = self.get_current_date_log_filename()
            file = open(path_log + filename, "a+");
            current_dt = self.get_current_datetime()
            file.write(current_dt + " " + message + "\n");
            file.close()
        except Exception as ex:
            print(ex)
            
    def get_current_datetime(self):
        return "[" + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S.%f") + "]"
    
    def auto_create_log_dir(self):
        if not os.path.exists(path_log):
            os.makedirs(path_log)
            
    def get_current_date_log_filename(self):
        return datetime.datetime.now().strftime("%d%m%y") + ".txt";
        
    def main(self) :        
        while True :
            self.auto_create_log_dir()
            barcode = str(input("scan Barcode : "))
            input_barcode = re.sub(r"\W", "", barcode)
            #print("input = " + str(input_barcode))
            if barcode != "" :
                self.check_ticket_validity(input_barcode)
            else :
                self.message = "Invalid Barcode : '" + input_barcode + "'."
                print(self.message)
                self.writeLog(self.message)
                self.play_sound(path_sound_file_invalid)
            print("\n")
