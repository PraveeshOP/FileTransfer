from socket import *

class Client:

    def openfile(filename):
        try:
            with open(filename, 'r') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            return None
        except IOError:
            print(f"Error: Could not read the file {filename}.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def main(fileName, ip, port):

        serverIP = ip
        serverPort = port

        clientSocket = socket(AF_INET, SOCK_DGRAM)

        message = input('Input lowercase sentence: ')

        serverAddress = (serverIP, serverPort)

        clientSocket.sendto(message.encode(), serverAddress)

        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

        print(f"Message received from {serverAddress}: {modifiedMessage.decode()}")

        clientSocket.close()


    if __name__ == '__main__':
        main()