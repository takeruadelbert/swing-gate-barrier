from desk_register import *

if __name__ == "__main__" :
    desk = DeskRegister()
    if desk.check_server_config() :
        desk.main()
    else :
        desk.play_sound(path_sound_file_invalid)
        print("Server configuration is not set properly.")