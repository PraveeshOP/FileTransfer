# UDP server

from socket import *
import _thread as thread
import sys

class Server:

    def main(ip, port):
        serverName = ip
        serverPort = port
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((serverName, serverPort))

        print('The server is ready to receive.......')

        message, clientAddress = serverSocket.recvfrom(2048)
        print(f"Received message from {clientAddress}: {message.decode()}")
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        serverSocket.close()

    if __name__ == '__main__':
        main()