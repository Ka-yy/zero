import socket
import os
import argparse
## send the file 

"""
TODO: make sure to use argparse to collect the Cli arguments 

"""

class client():

    def send_file(file_names, host='127.0.0.1', port=65432):
        try:
            # start the socket, bind it to a port and connect 
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            # Send files sequentially 
            for file_name in file_names:
                # confirm if the file exists 
                if not os.path.isfile(file_name):
                    print(f"File not found: {file_name}")
                    continue
                
                # show file size 
                file_size = os.path.getsize(file_name)

                #send the file size to the server 
                client_socket.send(str(file_size).encode())
                client_socket.recv(1024)  # Wait for ACK from server 

                with open(file_name, 'rb') as f:
                    bytes_sent = 0
                    while bytes_sent < file_size:
                        data = f.read(1024)
                        if not data:
                            break
                        client_socket.send(data)
                        bytes_sent += len(data)
                        print(f'Sending {file_name}: {bytes_sent / file_size * 100:.2f}%')
                
                response = client_socket.recv(1024).decode()
                print(response)
        except Exception as e:
            print(f'Error sending files: {e}')
        finally:
            client_socket.close()

    if __name__ == '__main__':
        print("Type 'send <IP/DNS>' followed by comma-separated filenames.")
        command = input("> ").strip().split()
        
        if command[0].lower() == 'send':
            host = command[1]
            files_to_send = command[2].split(',') if len(command) > 2 else []
            send_file([f.strip() for f in files_to_send], host)
