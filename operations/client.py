"""

ZERO CLIENT OPERATIONS

NOTE: Due to the architecture, the client is always sending code, while server is always receiving files

TODO: Start client server
TODO: Define methods for all the different client methods: ftp, sftp, http, https,  
                                                                    

"""
import socket
import os
import ftplib 
import requests 
from progress.bar import Bar
from paramiko import Transport, SFTPClient

class client():
    # initialize and show the supported transfer protocols
    def __init__(self):
        self.supported_protocols = {
            'ftp': self.ftp_send,
            'sftp': self.sftp_send,
            'http': self.http_send,
            'https': self.https_send,
        }

    # send using ftp with authentication
    def ftp_send(self, host, port, username, password, filePath):
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(host, port)
                ftp.login(username, password)
                with open(filePath, 'rb') as file:
                    ftp.storbinary(f'STOR {os.path.basename(filePath)}', file)
                print(f"file {filePath} send successfully via FtP.")
        except Exception as e:
            print(f"Error sending file via FTP: {e}")

    '''
    Send using sftp with authentication(login, password)

    NOTE: The differnce between the two is that sftp creates an ssh session, 
    then uses ftp through the running ssh session 

    ''' 
    def sftp_send(self, host, port, username, password, filePath):
        try:
            
            transport = Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = SFTPClient.from_transport(transport)
            sftp.put(filePath, os.path.basename(filePath))
            print(f"file {filePath} send successfully via SFTP.")
            transport.close()
        except Exception as e:
            print(f"Error sending file via SFTP: {e}")


    '''
    send using http POST request
    ''' 
    def http_send(self, url, filePath):
        try:
            with open(filePath, 'rb') as file:
                files = {'file':file}
                response = requests.post(url, files=files)
            if response.status_code ==200:
                print(f"File{filePath} sent successfully via HTTP.")
            else:
                print(f"Error sending file. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending file via Http: {e}")


    # send using https 
    def https_send(self, url, filePath):
        # https and http use the EXact same method, just a different url scheme/type
        self.http_send(url, filePath)

    def send_files(self, protocol, **kwargs):
        if protocol not in self.supported_protocols:
            print("unsupported protocol used, try using the correct protocol")
            self.supported_protocols[protocol](**kwargs)
        else:
            print(f"Unsupported protocol: {protocol}")