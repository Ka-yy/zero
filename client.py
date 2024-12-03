import socket;

s= socket.socket();
host = input(str("Please enter the host address of the sender.  "))
port = 8080;
s.connect((host,port))

print("Connected....")