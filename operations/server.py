import socket 
import os 
import threading 
import argparse 
import sys 

"""
TODO: startt debugging from "bytesReceived" instances, itll help alot 
TODO: we will decide where the "tempfilepath" is later, the file will be stored in the TEMP file in the cimputer then transferred into the
destinatio filder later 
"""
class server():
	# start the server and bind it to (host, port)    	
	def startServer(host='127.0.0.1', port=64532):
		serverSocket = socket.sockeet(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind((host, port))                    
		print(f'Server listening on {host}:{port}')                   
		while True:                                                  
			conn, addr = serverSocket.accept()
			threading.Thread(target=handleClient, args=(conn, addr)).start()\
			

		if __name__ == '__main__':
			print("Type receive to start the server.")
			command = input(">")
		if command.strip().lower() == 'receive':
				command = input(">")	



	def handleClient(conn, addr):
		# connect to the client
		print(f'Connection established with {addr}')
		conn.send(b'Connected to the server. Which file(s) do you wish to send? (comma-seperated paths)\n')
		
		filesToReceive = conn.recv(1024).decode().strip().split(',')

		for fileName in filesToReceive:
			fileName = fileName.strip()
			try: 
				conn.send(b'ACK')
				fileSize = int(conn.recv(1024).decode())
				conn.send(b'ACK')

				with open(tempFilePath, 'wb') as f:
					bytesReceived = 0 
					while bytesReceived < fileSize:
							data = conn.recv(1024)
					if not data:
						break
					f.write(data)
					bytesReceived += len(data)
					print(f'Received {fileName}: {bytesReceived / {fileSize} *100: .2f}%')

					if bytesReceived == fileSize:
						os.rename(tempFilePath, fileName)
						# MOve to the final destination
						print(f'Received complete: {fileName}')
						conn.send(b'Send complete ')
					else:
						os.remove(tempFilePath)
						# Delete incomplete file 
						print(f'Received incomplete: {fileName}. File Deleted')
			except Exception as e:
				print(f'Error receiving {fileName}: {e}') 
		conn.close()

