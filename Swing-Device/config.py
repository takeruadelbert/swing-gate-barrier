# For Server Configuration
ip_address_server = "http://192.168.88.210:4003"
url_check_ticket = "/flap"
timeout_connection = 5 # in second(s)
retry_connect = 3 # in second(s)

# GPIO to Relay
relay_pin = 2
delay_time = 0.5 # in second(s)

# sound file(s)
temp = "/home/pi/Documents/swing-gate-barrier/Swing-Device/files/sounds/"
path_sound_file_success = temp + "success.wav"
path_sound_file_invalid = temp + "invalid.wav"
path_sound_file_error_conn = temp + "error_connection.wav"
path_sound_file_error_timeout = temp + "error_timeout.wav"
path_sound_file_error_http = temp + "error_http.wav"

# Device Log
path_log = "/home/pi/Documents/swing-gate-barrier/Swing-Device/log/"