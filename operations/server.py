"""
ZERO server operations

NOTE: Due to the architecture, the client is always sending code, while server is always receiving files
 
TODO: we will decide where the "tempfilepath" is later, the file will be stored in the TEMP file in the cimputer then transferred into the
destinatio filder later 

"""

import argparse
from client import client
from server import Server
import sys
from getpass import getpass

def start_server_by_protocol(protocol):
    server = Server()  # Uses default host='0.0.0.0'
    if protocol == 'ftp':
        server.start_ftp_server()
    elif protocol == 'sftp':
        server.start_sftp_server()
    elif protocol == 'http':
        server.start_http_server()
    elif protocol == 'https':
        server.start_https_server()

def main():
    parser = argparse.ArgumentParser(description='Zero File Transfer Tool')
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--send', '-s', action='store_true', help='Send files')
    mode_group.add_argument('--receive', '-r', action='store_true', help='Receive files')
    
    parser.add_argument('--protocol', '-p', choices=['ftp', 'sftp', 'http', 'https'],
                      required=True, help='Transfer protocol to use')
    
    # Only add these arguments if we're in send mode
    send_group = parser.add_argument_group('send mode arguments')
    send_group.add_argument('--host', help='Target host address (only for send mode)')
    send_group.add_argument('--port', type=int, help='Port number (only for send mode)')
    send_group.add_argument('--username', '-u', help='Username for authentication (only for send mode)')
    send_group.add_argument('--file', '-f', help='Path to file for sending (only for send mode)')
    
    args = parser.parse_args()

    if args.send:
        if not all([args.host, args.file]):
            parser.error("Send mode requires --host and --file arguments")
        
        c = client()
        
        if args.protocol in ['ftp', 'sftp']:
            if not args.username:
                args.username = input("Username: ")
            password = getpass("Password: ")
            
            if not args.port:
                args.port = 21 if args.protocol == 'ftp' else 22
                
            if args.protocol == 'ftp':
                c.ftp_send(args.host, args.port, args.username, password, args.file)
            else:
                c.sftp_send(args.host, args.port, args.username, password, args.file)
        else:
            url = f"{args.protocol}://{args.host}"
            if args.port:
                url += f":{args.port}"
            url += "/upload"
            
            if args.protocol == 'http':
                c.http_send(url, args.file)
            else:
                c.https_send(url, args.file)
    
    else:  # receive mode
        print(f"Starting {args.protocol.upper()} server...")
        start_server_by_protocol(args.protocol)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)