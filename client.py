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

        #clientSocket.settimeout(1)  # Set a timeout for the socket operations
        
        active_connection = True # if the connection is active

        clientSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
        serverSocket = (serverIP, serverPort)
        print("Connection Establishment Phase: \n")
        
        # Send a SYN packet to the server
        syn = Packets.create_packet(0, 0, 8, 0, b'')
        clientSocket.sendto(syn, serverSocket)
        print("SYN packet is sent")

        try:
            while True:
                # Receive data from the server
                packet_from_server, serverAddress = clientSocket.recvfrom(1000)

                #Divide the packet into header and data
                packet_header = packet_from_server[:8]

                # Unpack the received packet
                sequence_number, acknowledgment_number, flags, window = Packets.parse_header(packet_header)

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
                required_ack = 1
                while (active_connection):
                    # Receive data from the server
                    packet_from_server, serverAddress = clientSocket.recvfrom(1000)

                    #Divide the packet into header and data
                    packet_header = packet_from_server[:8]

                    # Unpack the received packet
                    s_sequence_number, s_acknowledgment_number, s_flags, s_window = Packets.parse_header(packet_header)

                    # Read 992 bytes of data from the file
                    data = file.read(992)
                    if not data:
                        print("DATA Finished\n")
                        print("Connection Teardown:\n")
                        fin = Packets.create_packet(0, 0, 2, 0, b'')
                        clientSocket.sendto(fin, serverSocket)
                        print("FIN packet is sent")
                        active_connection = False
                        break
                    
                    elif (required_ack == s_acknowledgment_number):
                        # msg now holds a packet, including our custom header and data
                        print("Acknowledgment number is ", s_acknowledgment_number)

                        msg = Packets.create_packet(s_acknowledgment_number, s_acknowledgment_number-1, 0, 0, data)
                        # Send the packet to the server
                        clientSocket.sendto(msg, serverSocket)
                        print(f"{Client.now()} -- packet with seq = {s_acknowledgment_number} is sent")
                        
                        #Increment the required_ack
                        required_ack += 1
                        print(f"Requested packet {required_ack}")
                        continue
            
            while True:
                # Receive data from the server
                packet_header, serverAddress = clientSocket.recvfrom(1000)

                # Unpack the received packet
                seq, ack, flags, win = Packets.parse_header(packet_header)

                # Check the flags to determine the type of packet received
                syn, ack, fin = Packets.parse_flags(flags)

                if (fin == 2 and ack == 4):
                    print("FIN-ACK packet is received")
                    # Send a response back to the server
                    print("Connection Closes\n")
                    break 

        except KeyboardInterrupt:
            print("Connection Terminated")

        clientSocket.close()

if __name__ == "__main__":
    Client.main()