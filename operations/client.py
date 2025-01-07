import socket
import os
import ftplib  # Import FTP module for FTP transfers
import requests  # Import requests module for HTTP/HTTPS transfers
from paramiko import Transport, SFTPClient  # Import paramiko for SFTP transfers

class client():
    def __init__(self):
        # Supported protocols for file transfer and corresponding methods
        self.supported_protocols = {
            'ftp': self.ftp_send,  # Maps 'ftp' to the ftp_send method
            'sftp': self.sftp_send,  # Maps 'sftp' to the sftp_send method
            'http': self.http_send,  # Maps 'http' to the http_send method
            'https': self.https_send,  # Maps 'https' to the https_send method
        }

    # FTP transfer method with authentication (username & password)
    def ftp_send(self, host, port, username, password, filePath):
        """
        This method sends a file using the FTP protocol. 
        It connects to the server, logs in with the given credentials,
        and uploads the file.
        """
        try:
            with ftplib.FTP() as ftp:
                # Connect to the FTP server
                ftp.connect(host, port)
                # Login with the provided credentials
                ftp.login(username, password)
                # Open the file in binary read mode and send it to the server
                with open(filePath, 'rb') as file:
                    # Store the file with the same name on the server
                    ftp.storbinary(f'STOR {os.path.basename(filePath)}', file)
                print(f"File {filePath} sent successfully via FTP.")
        except Exception as e:
            print(f"Error sending file via FTP: {e}")

    '''
    SFTP transfer method with authentication (login, password)
    NOTE: The main difference between FTP and SFTP is that SFTP operates over SSH.
    This creates a secure session before transferring the file.
    '''
    def sftp_send(self, host, port, username, password, filePath):
        """
        This method sends a file using the SFTP protocol over an SSH session.
        It creates an SSH transport connection, authenticates using provided credentials,
        and uploads the file.
        """
        try:
            # Establish an SSH transport connection to the server
            transport = Transport((host, port))
            transport.connect(username=username, password=password)
            # Create an SFTP client from the transport connection
            sftp = SFTPClient.from_transport(transport)
            # Upload the file to the server
            sftp.put(filePath, os.path.basename(filePath))  # Upload the file with the same name
            print(f"File {filePath} sent successfully via SFTP.")
            # Close the transport connection after the file transfer is complete
            transport.close()
        except Exception as e:
            print(f"Error sending file via SFTP: {e}")

    '''
    HTTP transfer method with POST request
    NOTE: This sends a file as part of a multipart form-data request to the given URL.
    '''
    def http_send(self, url, filePath):
        """
        This method sends a file using an HTTP POST request to the server.
        The file is uploaded as part of the request's body.
        """
        try:
            # Open the file in binary read mode and prepare it for sending
            with open(filePath, 'rb') as file:
                files = {'file': file}  # The file to be uploaded
                # Send the POST request with the file attached
                response = requests.post(url, files=files)
            # Check the response status code to confirm if the upload was successful
            if response.status_code == 200:
                print(f"File {filePath} sent successfully via HTTP.")
            else:
                print(f"Error sending file. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending file via HTTP: {e}")

    # HTTPS transfer method (essentially the same as HTTP)
    def https_send(self, url, filePath):
        """
        This method sends a file using HTTPS, which is essentially the same
        as sending via HTTP but uses the HTTPS protocol for secure communication.
        """
        # Simply use the same logic as HTTP since the difference is only the URL scheme
        self.http_send(url, filePath)

    # General send method to choose the correct protocol and send the file
    def send_files(self, protocol, **kwargs):
        """
        This method is used to select the file transfer protocol and call the corresponding
        method to send the file. It checks if the protocol is supported and passes the 
        required arguments to the corresponding transfer method.
        """
        if protocol not in self.supported_protocols:
            print(f"Unsupported protocol: {protocol}")  # If the protocol is not in the supported list
        else:
            # Call the appropriate method based on the protocol
            self.supported_protocols[protocol](**kwargs)
