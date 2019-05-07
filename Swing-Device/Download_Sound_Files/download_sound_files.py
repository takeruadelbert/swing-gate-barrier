from download_sound_file_config import *
import requests, sys

class DownloadSoundFile :
    def get_response_server(self):
        try :
            print("Connecting to server ...")
            response = requests.get(url, timeout=timeout_connection, stream=True)
            response.raise_for_status()
            data_json = response.json()
            if data_json['status'] == 206 :
                data = data_json['data']
                for name, url_file in data.items() :
                    self.download_sound_file(name, response)
                print("Finished.")
            else :
                print("failed")
        except requests.exceptions.ConnectionError as errc:
            print("Cannot establish connection to server. Please configure the server properly.")
            sys.exit(1)
        except requests.exceptions.Timeout as errt :
            print(errt)
            sys.exit(1)
        except requests.exceptions.HTTPError as err :
            print(err)
            sys.exit(1)
    
    def download_sound_file(self, filename, response):
        print("Downloading file : '" + filename + "' ...")
        total_length = response.headers.get("content-length")
        if total_length is None :
            print("content length = " + total_length)
        else :
            try :
                full_url_sound_file = url_download_sound_file + filename
                r = requests.get(full_url_sound_file, timeout=timeout_connection)
                with open(dir_sound_file + filename, 'wb') as f :
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096) :
                        dl += len(data)
                        f.write(r.content)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                        sys.stdout.flush()
                        print("\n")
                f.close()
            except requests.exceptions.ConnectionError as errc:
                print("Cannot establish connection to server. Please configure the server properly.")
                sys.exit(1)
            except requests.exceptions.Timeout as errt :
                print(errt)
                sys.exit(1)
            except IOError:
                print("No such created directory : ", "'" + dir_sound_file + "'. Make sure the directory exists/created.")
                sys.exit(1)
        
    def main(self) :
        self.get_response_server()