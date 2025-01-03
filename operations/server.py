"""
ZERO SERVER OPERATIONS

NOTE: Due to the architecture, the client is always sending code, while server is always receiving files
 
TODO: we will decide where the "tempfilepath" is later, the file will be stored in the TEMP file in the cimputer then transferred into the
destinatio filder later 

"""
import os # for system ooperations
import socket # for sokcet operatioms 
from pyftpdlib.authorizers import DummyAuthorizer # for ftp authorization 
from pyftpdlib.handlers import FTPHandler # for ftp handling
from pyftpdlib.servers import FTPServer # for starting the ftp server
import paramiko    # to automatate the sftp operations 
from flask import Flask, request  # for http(s) requests
from werkzeug.utils import secure_filename # for secure http requests
import threading  # for async operations 


class Server:
	# initialize the class
    def __init__(self, host='0.0.0.0', ftp_port=21, sftp_port=22, http_port=80, https_port=443):
        self.host = host
        self.ftp_port = ftp_port
        self.sftp_port = sftp_port
        self.http_port = http_port
        self.https_port = https_port
        self.upload_dir = 'uploads'
        os.makedirs(self.upload_dir, exist_ok=True)

	# start the FTP server
    def start_ftp_server(self):
        authorizer = DummyAuthorizer()
        authorizer.add_anonymous(self.upload_dir, perm='elradfmwMT')

        handler = FTPHandler
        handler.authorizer = authorizer

        server = FTPServer((self.host, self.ftp_port), handler)
        print(f"FTP server started on {self.host}:{self.ftp_port}")
        server.serve_forever()

	# start the sftp server 
    def start_sftp_server(self):
		# start the server 
        class SFTPServer(paramiko.ServerInterface):
            def check_auth_password(self, username, password):
                return paramiko.AUTH_SUCCESSFUL

			# check the request channel 
            def check_channel_request(self, kind, chanid):
                return paramiko.OPEN_SUCCEEDED

		# open the socket connection, bind it and start the server 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.sftp_port))
        server_socket.listen(5)

        print(f"SFTP server started on {self.host}:{self.sftp_port}")

		# start the server loop
        while True:
			# accept the connection from the client 
            client, addr = server_socket.accept()
			# receive the files from the client
            transport = paramiko.Transport(client, addr)
			# generate server key for authentication
            transport.add_server_key(paramiko.RSAKey.generate(2048))
            transport.set_subsystem_handler('sftp', paramiko.SFTPServer, SFTPServer)
            server = SFTPServer()
            transport.start_server(server=server)

            channel = transport.accept(1)
            if channel is None:
                continue

            sftp = paramiko.SFTPServer(channel)
            while True:
                try:
                    sftp.server_accept()
                except:
                    break
	# Flask http server will be used to start the http  server 
    def start_http_server(self):
        app = Flask(__name__)

        @app.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return 'No file part', 400
            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.upload_dir, filename))
                return 'File uploaded successfully', 200

        app.run(host=self.host, port=self.http_port)

    def start_https_server(self):
        # For HTTPS, you need to generate SSL certificates
        # This is a placeholder. In a real-world scenario, you'd use proper SSL certificates
        app = Flask(__name__)

        @app.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return 'No file part', 400
            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.upload_dir, filename))
                return 'File uploaded successfully', 200

        app.run(host=self.host, port=self.https_port, ssl_context='adhoc')

    def start(self):
        threads = [
            threading.Thread(target=self.start_ftp_server),
            threading.Thread(target=self.start_sftp_server),
            threading.Thread(target=self.start_http_server),
            threading.Thread(target=self.start_https_server)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    server = Server()
    server.start()