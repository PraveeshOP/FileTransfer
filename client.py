# UDP client

from socket import *

def main():

    serverIP = '0.0.0.0'
    serverPort = 12000

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    message = input('Input lowercase sentence: ')

    serverAddress = (serverIP, serverPort)

    clientSocket.sendto(message.encode(), serverAddress)

    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    print(f"Message received from {serverAddress}: {modifiedMessage.decode()}")

    clientSocket.close()


if __name__ == '__main__':
    main()