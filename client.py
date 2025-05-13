from socket import *
from packets import Packets

class Client:

    @staticmethod
    def main(filename, serverIP, serverPort):
        clientSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
        serverSocket = (serverIP, serverPort)
        print("Connection Establishment Phase: \n")
        
        # Send a SYN packet to the server
        syn = Packets.create_packet(0, 0, 8, 0, b'')
        clientSocket.sendto(syn, serverSocket)

        try:
            while True:
                # Receive data from the server
                packet_header, serverAddress = clientSocket.recvfrom(1024)

                # Unpack the received packet
                seq, ack, flags, win = Packets.parse_header(packet_header)

                # Check the flags to determine the type of packet received
                syn, ack, fin = Packets.parse_flags(flags)

                if (syn == 8 and ack == 4):
                    print("SYN-ACK packet is received")
                    # Send a response back to the server
                    ack = Packets.create_packet(0, 0, 4, 0, b'')
                    clientSocket.sendto(ack, serverSocket)
                    print("ACK packet is sent")
                    print("Connection established\n")
                    break
            # File Transfer Phase
            print("Data Transfer:\n")
            

        except Exception as KeyboardInterrupt:
            print("Connection Terminated")

        clientSocket.close()

if __name__ == "__main__":
    Client.main()