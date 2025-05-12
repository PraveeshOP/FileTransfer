import argparse
from server import Server

def main():
    ip = "127.0.0.1"
    port = 12000

    Server.main(ip, port)

if __name__ == "__main__":
    main()