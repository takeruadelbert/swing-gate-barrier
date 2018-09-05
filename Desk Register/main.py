from desk_register import *

if __name__ == "__main__" :
    desk = DeskRegister(ip_address_server, url, timeout_connection)
    if desk.check_server_config() :
        desk.main()
    else :
        print("Server configuration is not set properly.")
    