import os
from flask import Flask, request
import paramiko
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class Server:
    def __init__(self):
        # Setting up the server host and port
        self.host = '0.0.0.0'  # The server will listen on all available network interfaces (all IP addresses)
        self.port = 21  # Default FTP port
        self.upload_folder = "uploads"  # Directory where uploaded files will be stored

        # Create the upload folder if it doesn't exist
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    # FTP Server Setup
    def start_ftp_server(self):
        """
        This function sets up and starts an FTP server that allows file transfers
        using FTP protocol. It uses pyftpdlib library for FTP functionality.
        """
        # Creating an authorizer object to handle user authentication
        authorizer = DummyAuthorizer()
        # Adding a user with 'user' as username, 'password' as password, and upload folder as home directory
        # 'elradfmw' gives the user permissions like reading, writing, etc.
        authorizer.add_user('user', 'password', self.upload_folder, perm='elradfmw')
        
        # Creating a handler for FTP requests
        handler = FTPHandler
        handler.authorizer = authorizer  # Linking the authorizer to the handler
        # Creating an FTP server object that listens on the specified host and port
        server = FTPServer((self.host, self.port), handler)
        print(f"Starting FTP server at {self.host}:{self.port}")
        # Starting the server and it will keep running
        server.serve_forever()

    # SFTP Server Setup using Paramiko (secure FTP over SSH)
    def start_sftp_server(self):
        """
        This function sets up an SFTP server using the Paramiko library.
        SFTP is a secure file transfer protocol that works over SSH.
        """
        try:
            # Creating an SFTP server instance using Paramiko
            server = paramiko.SFTPServer(self.upload_folder)
            server.start(self.host, self.port)
            print(f"SFTP Server started on {self.host}:{self.port}")
        except Exception as e:
            print(f"Error starting SFTP server: {e}")

    # HTTP Server Setup using Flask (for uploading files via HTTP POST requests)
    def start_http_server(self):
        """
        This function sets up a simple HTTP server using Flask.
        The server will allow file uploads via HTTP POST requests to the /upload endpoint.
        """
        app = Flask(__name__)  # Initializing the Flask application

        # Route for uploading files
        @app.route('/upload', methods=['POST'])
        def upload_file():
            # Check if the file part exists in the request
            if 'file' not in request.files:
                return 'No file part', 400  # Return error if no file is attached
            
            file = request.files['file']
            if file.filename == '':  # Check if no file is selected
                return 'No selected file', 400  # Return error if no file is selected
            
            # Save the uploaded file in the upload folder
            file.save(os.path.join(self.upload_folder, file.filename))
            return f"File {file.filename} uploaded successfully", 200  # Return success message

        # Run the Flask application on the given host and port
        app.run(host=self.host, port=self.port)
        print(f"Starting HTTP server at {self.host}:{self.port}")

    # HTTPS Server Setup (Same as HTTP but with SSL encryption for secure transfers)
    def start_https_server(self):
        """
        This function sets up an HTTPS server using Flask. It is similar to HTTP
        but provides an SSL-encrypted connection.
        """
        app = Flask(__name__)

        # Route for uploading files
        @app.route('/upload', methods=['POST'])
        def upload_file():
            # Check if the file part exists in the request
            if 'file' not in request.files:
                return 'No file part', 400
            
            file = request.files['file']
            if file.filename == '':  # Check if no file is selected
                return 'No selected file', 400
            
            # Save the uploaded file in the upload folder
            file.save(os.path.join(self.upload_folder, file.filename))
            return f"File {file.filename} uploaded successfully", 200

        # Run the Flask application with SSL context for HTTPS
        # SSL certificates (cert.pem and key.pem) are required for HTTPS to work
        app.run(host=self.host, port=self.port, ssl_context=('cert.pem', 'key.pem'))
        print(f"Starting HTTPS server at {self.host}:{self.port}")

# This function is used to start the server based on the selected protocol
def start_server_by_protocol(protocol):
    """
    This function checks the selected protocol (ftp, sftp, http, https) and starts the corresponding server.
    """
    server = Server()  # Creating a Server instance
    if protocol == 'ftp':
        server.start_ftp_server()  # Start FTP server if protocol is FTP
    elif protocol == 'sftp':
        server.start_sftp_server()  # Start SFTP server if protocol is SFTP
    elif protocol == 'http':
        server.start_http_server()  # Start HTTP server if protocol is HTTP
    elif protocol == 'https':
        server.start_https_server()  # Start HTTPS server if protocol is HTTPS
    else:
        print(f"Unsupported protocol: {protocol}")  # Print error message if protocol is not supported

# Main entry point for the server
if __name__ == "__main__":
    # Argument parsing for running the server
    import argparse
    parser = argparse.ArgumentParser(description="Zero File Transfer Tool")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--send', '-s', action='store_true', help='Send files')
    mode_group.add_argument('--receive', '-r', action='store_true', help='Receive files')

    parser.add_argument('--protocol', '-p', choices=['ftp', 'sftp', 'http', 'https'], required=True, help='Transfer protocol to use')
    
    # Only add these arguments if we're in send mode
    send_group = parser.add_argument_group('send mode arguments')
    send_group.add_argument('--host', help='Target host address (only for send mode)')
    send_group.add_argument('--port', type=int, help='Port number (only for send mode)')
    send_group.add_argument('--username', '-u', help='Username for authentication (only for send mode)')
    send_group.add_argument('--file', '-f', help='Path to file for sending (only for send mode)')
    
    args = parser.parse_args()

    if args.send:
        # This part is handled by the client side (you can implement the sending functionality here)
        pass  # Send functionality will be implemented in the client

    else:  # If receive mode is selected, start the server based on the protocol
        print(f"Starting {args.protocol.upper()} server...")
        start_server_by_protocol(args.protocol)  # Start the server with the selected protocol
