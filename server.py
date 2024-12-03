import socket;
s = socket.socket() ##* Initialize the socket
host = socket.gethostname(); ##* Connection for client.py 
port = 8080
s.bind((host,port)) ##* Bind port number and IP address
s.listen(1) ##? 1 means 1 connection at a time
print("Waiting for a connection")
conn , addr = s.accept() #? s is the object that will be accepted
print(addr, "Has connected to the server")