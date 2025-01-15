# import argparse   
""" 
 TODO: make a terminal help for the usage of the app 
     the usage of the app should look like:  
     '''shell 
         ## Input  
         zero --help 
         # OUTPUT  
         Usage: select send or receive to send/recieve files  
         arguments 
         --send, -s [send] 
                     [Protocols] 
                     -ftp  
                     -sftp 
                     -http 
                     -htttps  
                         --ip:port/dns:port [location of receiver] 
                             -- path/to/file(s) 
         --receive, -r [receive] 
     ''' 

 NOTE: to use the predefinded functions, create a new object and then call the methods 
 """ 


# import argparse // no need for this anymore 
from operations.client import client 
from operations.server import Server
import sys
from getpass import getpass
import cmd
import os 


class ZeroShell(cmd.Cmd):
    intro = """
    =========================================
    Zero File Transfer Tool - Interactive Shell
    Type 'help' or '?' to list commands.
    Type 'exit' or 'quit' to exit.
    =========================================
    """
    prompt = 'zero> '
    
    def __init__(self):
        super().__init__()
        self.client = client()
        self.server = Server()
        self.current_mode = None
    
    def do_send(self, arg):
        """
        Start send mode with specified protocol:
        Usage: send <protocol>
        Protocols: ftp, sftp, http, https
        Example: send ftp
        """
        protocol = arg.lower().strip()
        if protocol not in ['ftp', 'sftp', 'http', 'https']:
            print("Invalid protocol. Use: ftp, sftp, http, or https")
            return
            
        self.current_mode = 'send'
        host = input("Host: ")
        
        if protocol in ['ftp', 'sftp']:
            port = input("Port (default: 21 for ftp, 22 for sftp): ")
            port = int(port) if port else (21 if protocol == 'ftp' else 22)
            username = input("Username: ")
            password = getpass("Password: ")
            file_path = input("File path: ")
            
            if protocol == 'ftp':
                self.client.ftp_send(host, port, username, password, file_path)
            else:
                self.client.sftp_send(host, port, username, password, file_path)
        else:
            port = input("Port (optional): ")
            file_path = input("File path: ")
            url = f"{protocol}://{host}"
            if port:
                url += f":{port}"
            url += "/upload"
            
            if protocol == 'http':
                self.client.http_send(url, file_path)
            else:
                self.client.https_send(url, file_path)

    def do_receive(self, arg):
        """
        Start receive mode (server) with specified protocol:
        Usage: receive <protocol>
        Protocols: ftp, sftp, http, https
        Example: receive ftp
        """
        protocol = arg.lower().strip()
        if protocol not in ['ftp', 'sftp', 'http', 'https']:
            print("Invalid protocol. Use: ftp, sftp, http, or https")
            return
            
        self.current_mode = 'receive'
        print(f"Starting {protocol.upper()} server...")
        
        try:
            if protocol == 'ftp':
                self.server.start_ftp_server()
            elif protocol == 'sftp':
                self.server.start_sftp_server()
            elif protocol == 'http':
                self.server.start_http_server()
            elif protocol == 'https':
                self.server.start_https_server()
        except KeyboardInterrupt:
            print("\nServer stopped")
        except Exception as e:
            print(f"Error: {e}")

    def do_status(self, arg):
        """Show current mode and status"""
        if self.current_mode:
            print(f"Current mode: {self.current_mode}")
        else:
            print("No active mode")

    def do_clear(self, arg):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_exit(self, arg):
        """Exit the program"""
        print("Goodbye!")
        return True
        
    def do_quit(self, arg):
        """Exit the program"""
        return self.do_exit(arg)
        
    def default(self, line):
        """Handle unknown commands"""
        print(f"Unknown command: {line}")
        print("Type 'help' or '?' to see available commands")

def main():
    try:
        ZeroShell().cmdloop()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()