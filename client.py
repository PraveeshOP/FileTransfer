from socket import *

class Client:

    @staticmethod
    def main(filename, serverIP, serverPort):
        clientSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
        serverSocket = (serverIP, serverPort)
        print("Connection Establishment Phase: \n")
        
        #SYN packet
        syn = "SYN packet is sent"
        clientSocket.sendto(syn.encode(), serverSocket)
        print(syn)

        while True:
            response, serverAddress = clientSocket.recvfrom(1024)
            response = response.decode()
            if (response == "SYN-ACK packet is sent"):
                print("SYN-ACK packet is received")
                # Send a response back to the server
                clientSocket.sendto("ACK packet is sent".encode(), serverSocket)
                print("ACK packet is sent")

            elif (response == "Connection established"):
                print("Connection established\n")
                break

        clientSocket.close()

if __name__ == "__main__":
    Client.main()