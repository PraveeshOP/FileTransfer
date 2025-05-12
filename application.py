from server import Server
from client import Client
import argparse

parser = argparse.ArgumentParser(description="This is the whole application!")

# Optional arguments for roles
parser.add_argument('-s', '--server', action='store_true', help="Run as server")
parser.add_argument('-c', '--client', action='store_true', help="Run as client")

# Optional filename for the client
parser.add_argument('-f', '--filename', metavar='', type=str, help="Please provide the filename")

# Required arguments for IP and port
parser.add_argument('-i', '--IP', metavar='', type=str, required=True, help="Please provide the IP address of the server")
parser.add_argument('-p', '--port', metavar='', type=int, required=True, help="Please provide the port number of the server")

args = parser.parse_args()

def main():
    if args.server:
        Server.main(args.IP, args.port)
        # Call your Server.main() here
    elif args.client:
        if not args.filename:
            print("Error: Please provide a filename using the -f or --filename argument.")
            return
        Client.main(args.filename, args.IP, args.port)
        # Call your Client.main() here
    else:
        print("Error: Please specify a role. Use -s for server or -c for client. Use -h for help.")

if __name__ == '__main__':
    main()