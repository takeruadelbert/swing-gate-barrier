# For Server Configuration
ip_address_server = "http://192.168.88.201"
url_check_ticket = "/eport/api/validate-ticket"
timeout_connection = 5 # in second(s)
retry_connect = 3 # in second(s)

# GPIO to Relay
relay_pin = 2
delay_time = 0.5 # in second(s)

# sound file(s)
path_sound_file_success = "/home/pi/python/files/sounds/success.wav"
path_sound_file_invalid = "/home/pi/python/files/sounds/invalid.wav"
path_sound_file_error_conn = "/home/pi/python/files/sounds/error_connection.wav"
path_sound_file_error_timeout = "/home/pi/python/files/sounds/error_timeout.wav"
path_sound_file_error_http = "/home/pi/python/files/sounds/error_http.wav"