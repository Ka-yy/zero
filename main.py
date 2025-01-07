import argparse
from operations.client import client
from operations.server import Server
import sys
from getpass import getpass

def show_quick_help():
    print("Zero - A File Transfer Tool")
    print("Usage: zero [--help] [--send | --receive] [options]")
    print("\nUse 'zero --help' for detailed usage information")

def main():
    if len(sys.argv) == 1:
        show_quick_help()
        return

    # Setup ArgumentParser
    parser = argparse.ArgumentParser(
        description='Zero - File Transfer Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Example:
    Send file using FTP:
        zero -s -p ftp --host ftp.example.com --file path/to/file
  
    Start SFTP receiver:
        zero -r -p sftp
        
Supported Protocols:
    FTP   : Basic FTP transfer (requires authentication)
    SFTP  : Secure FTP over SSH
    HTTP  : Basic HTTP transfer
    HTTPS : Secure HTTP transfer"""
    )
    
    # Add mutually exclusive options for send/receive
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--send', '-s', action='store_true', help='Send files to a remote server')
    mode_group.add_argument('--receive', '-r', action='store_true', help='Start server to receive files')
    
    # Arguments for protocol and connection
    parser.add_argument('--protocol', '-p', choices=['ftp', 'sftp', 'http', 'https'],
                      help='Transfer protocol')
    parser.add_argument('--host', help='Target host address')
    parser.add_argument('--port', type=int, help='Port number (default: protocol specific)')
    parser.add_argument('--username', '-u', help='Username for authentication')
    parser.add_argument('--file', '-f', help='Path to file(s) for sending')

    args = parser.parse_args()

    # Sending files logic
    if args.send:
        if not all([args.protocol, args.host, args.file]):
            parser.error("Send mode requires --protocol, --host, and --file arguments")
        
        c = client()
        
        # Handle FTP and SFTP (which require authentication)
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
        
        # Handle HTTP and HTTPS (which do not require authentication)
        else:
            url = f"{args.protocol}://{args.host}"
            if args.port:
                url += f":{args.port}"
            url += "/upload"
            
            if args.protocol == 'http':
                c.http_send(url, args.file)
            else:
                c.https_send(url, args.file)
    
    # Receiving files logic (start server)
    else:
        print("Starting server...")
        server = Server()
        
        # Start the server for the selected protocol
        if args.protocol == 'ftp':
            server.start_ftp_server()
        elif args.protocol == 'sftp':
            server.start_sftp_server()
        elif args.protocol == 'http':
            server.start_http_server()
        elif args.protocol == 'https':
            server.start_https_server()
        else:
            print("Unsupported protocol for receiving files.")
            sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
