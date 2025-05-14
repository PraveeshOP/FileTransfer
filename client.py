from socket import *
from packets import Packets
from datetime import datetime

class Client:

    @staticmethod
    def now():
        # Get the current time
        now = datetime.now()

        # Format the time to include hours, minutes, seconds, and microseconds
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond}"
        return formatted_time

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

            with open(filename, "rb") as file:
                sequence_number = 1
                while True:
                    # Read 992 bytes of data from the file
                    data = file.read(992)
                    if not data:
                        break
                    # Create a packet with the data
                    acknowledgment_number = 0
                    window = 0
                    flags = 0
                    # msg now holds a packet, including our custom header and data
                    msg = Packets.create_packet(sequence_number, acknowledgment_number, flags, window, data)
                    # Print the data and increment the sequence number
                    sequence_number += 1
                    # Send the packet to the server
                    clientSocket.sendto(msg, serverSocket)
                    print(f"{Client.now()} -- packet with seq = {sequence_number} is sent")

            clientSocket.sendto(data, serverSocket)            

        except Exception as KeyboardInterrupt:
            print("Connection Terminated")

        clientSocket.close()

if __name__ == "__main__":
    Client.main()