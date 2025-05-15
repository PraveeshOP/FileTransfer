from socket import *
from packets import Packets
from datetime import datetime
import sys

class Client:

    @staticmethod
    def now():
        # Get the current time
        now = datetime.now()

        # Format the time to include hours, minutes, seconds, and microseconds
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond}"
        return formatted_time

    @staticmethod
    def main(filename, serverIP, serverPort, windowSize):
        try:
            clientSocket = socket(AF_INET, SOCK_DGRAM)
            clientSocket.settimeout(0.4)  # Set timeout to 400ms
            serverSocket = (serverIP, serverPort)
            print("\nConnection Establishment Phase:\n")

            # Send SYN packet
            syn = Packets.create_packet(0, 0, 8, 0, b'')
            clientSocket.sendto(syn, serverSocket)
            print("SYN packet is sent")

            while True:
                try:
                    packet_from_server, _ = clientSocket.recvfrom(1000)
                    s_sequence_number, s_acknowledgment_number, flags, s_window = Packets.parse_header(packet_from_server[:8])
                    syn, ack, fin = Packets.parse_flags(flags)

                    if syn == 8 and ack == 4:
                        print("SYN-ACK packet is received")
                        # Send ACK packet
                        s_acknowledgment_number = Packets.create_packet(0, 0, 4, 0, b'')
                        clientSocket.sendto(s_acknowledgment_number, serverSocket)
                        print("ACK packet is sent")
                        print("Connection established\n")
                        windowSize = min(windowSize, s_window)  # Adjusting window size, the minimum among the server window and the client window is used
                        break
                except timeout:
                    print("\nConnection failed\n")
                    sys.exit()

            # File Transfer Phase
            print("Data Transfer:\n")
            with open(filename, "rb") as file:
                starting_sequence = 1
                next_seq = 1
                previous_seq = 0 #This is used to check the packet loss
                buffer = {} #This is the dictionary to hold the transmitted data that has not been acknowledge, it is used for the retransmission
                file_complete = False #Boolean to know weather the file is completely transferred or not

                while not file_complete or buffer: #This loops checks if the file is empty or the buffer is empty
                    # Send packets within the window
                    while (next_seq < starting_sequence + windowSize and not file_complete): #This loops sends the chunks according to the window size and also checks if the file is complete
                        data = file.read(992)
                        if not data:
                            file_complete = True
                            break
                        packet = Packets.create_packet(next_seq, next_seq-1, 0, 0, data) #Creating the packet with the sequence number and data from the file
                        clientSocket.sendto(packet, serverSocket) #Sending the data to the server socket
                        buffer[next_seq] = packet #The packets are saved in the buffer until they are acknowledge
                        print(f"{Client.now()} -- packet with seq = {next_seq} is sent, sliding window = {list(buffer.keys())}")
                        next_seq += 1

                    try:
                        # Receive ACK from the server
                        packet_from_server, _ = clientSocket.recvfrom(1000)
                        s_sequence_number, s_acknowledgment_number, flags, s_window = Packets.parse_header(packet_from_server[:8])
                        syn, ack, fin = Packets.parse_flags(flags)

                        if (ack == 4 and previous_seq != s_acknowledgment_number):
                            print(f"{Client.now()} -- ACK for packet = {s_acknowledgment_number} is received")
                            while (starting_sequence <= s_acknowledgment_number): #The loop to check of the sent sequence number is acknowledged by the server.
                                #If the sequence number is acknowledged the sequence number is removed from the buffer.
                                buffer.pop(starting_sequence, None) #None is used to handle the error if the key does not exist.  
                                starting_sequence += 1 #Incrementing the starting_sequence to check the acknowledgment number sent by the server
                                previous_seq += 1
                        elif (previous_seq == s_acknowledgment_number):
                            continue #If we get the acknolwgdement of the previous packet retransmitt the packet

                    except timeout:
                        # Resend all packets in the sliding window if the sent packets are not acknowleged until the occurance of the timeout.
                        print(f"{Client.now()} -- RTO occured")
                        #If the sequence number is not acknowleged
                        for seq in range(starting_sequence, next_seq): #The client retransmitts all the packects in the sliding window or buffer until the packets are acknowleged 
                            clientSocket.sendto(buffer[seq], serverSocket) #buffer[seq] contains all the packets present in the buffer
                            print(f"{Client.now()} -- retransmitting packet with seq = {seq}")

            # Connection Teardown
            print("Data Finished")
            print("\nConnection Teardown:\n")
            fin = Packets.create_packet(0, 0, 2, 0, b'')
            clientSocket.sendto(fin, serverSocket)
            print("FIN packet is sent")

            while True:
                try:
                    packet_from_server, _ = clientSocket.recvfrom(1000)
                    s_sequence_number, s_acknowledgment_number, flags, s_window = Packets.parse_header(packet_from_server[:8])
                    seq, ack, fin = Packets.parse_flags(flags)

                    if (fin == 2 and ack == 4): #If the timeout occures during the connection teardown phase
                        print("FIN-ACK packet is received")
                        print("Connection Closes\n")
                        break
                except timeout:
                    print("Timeout: Resending FIN packet")
                    clientSocket.sendto(fin, serverSocket)

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()
        except KeyboardInterrupt:
            print(f"Keyboard interrupt occured.")
            sys.exit()
        finally:
            clientSocket.close()
            sys.exit()
