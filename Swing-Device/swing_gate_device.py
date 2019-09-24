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

class SwingGate :
    def __init__(self) :
        self.relay = gpiozero.OutputDevice(relay_pin, active_high=False, initial_value=False, pin_factory=None)
        self.message = "";
        
    def check_ticket_validity(self, barcode) :
        hasError = False
        try :
            par = {"barcode" : barcode, "ipv4" : self.get_ip_address()}
            url = ip_address_server + url_check_ticket
            self.writeLog("Checking '" + barcode + "' ...")
            response = requests.post(url, json=par, timeout=timeout_connection)
            response.raise_for_status()
            data_json = response.json()
            self.message = data_json['message']
            self.writeLog("Getting Response ...")
            if data_json['status'] == 200 :
                self.relay.on()
                sleep(delay_time)
                self.play_sound(path_sound_file_success)
            else :
                self.play_sound(path_sound_file_invalid)
            self.relay.off()
        except requests.exceptions.ConnectionError as errc :
            hasError = True
            self.play_sound(path_sound_file_error_conn)
            self.message = "cannot establish connection to server. please setup the server properly."
        except requests.exceptions.Timeout as errt:
            hasError = True
            self.play_sound(path_sound_file_error_timeout)
            self.message = errt
        except requests.exceptions.HTTPError as err :
            hasError = True
            self.play_sound(path_sound_file_error_http)
            self.message = err
        except Exception as ex:
            hasError = True
            self.message = ex
            self.play_sound(path_sound_file_error_conn)
        finally:
            self.writeLog(self.message)
            if hasError:                
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
        return "[" + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + "]"
    
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
