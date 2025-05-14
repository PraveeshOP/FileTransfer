from socket import *
from packets import Packets
from datetime import datetime
import _thread as thread

class Server:
    
    @staticmethod
    def now():
        # Get the current time
        now = datetime.now()

        # Format the time to include hours, minutes, seconds, and microseconds
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond}"
        return formatted_time

    @staticmethod
    def handleClient(data, clientAddress, serverSocket):
        """
        Handles a single client request.
        """
        while True:
            required_seq = 1
            # Unpack the received packet_header
            packet_header = data[:8]
            seq, ack, flags, win = Packets.parse_header(packet_header)

            #packet data
            packet_data = data[8:]  # Extract the data part of the packet
            
            # Check the flags to determine the type of packet received
            syn, ack, fin = Packets.parse_flags(flags)

            if (syn == 8):
                print("SYN packet is received")
                # Send a response back to the client
                syn_ack = Packets.create_packet(0, 0, 12, 0, b'')
                serverSocket.sendto(syn_ack, clientAddress)
                print("SYN-ACK packet is sent")
                break
            
            elif (ack == 4):
                print("ACK packet is received")
                print("Connection established\n")
                break

            elif (fin == 2):
                print("FIN packet is received")
                # Send a response back to the client
                fin_ack = Packets.create_packet(0, 0, 6, 0, b'')
                serverSocket.sendto(fin_ack, clientAddress)
                print("FIN-ACK packet is sent")
                break

            elif (seq == required_seq):
                print(f"{Server.now()} -- packet {seq} is received")
                print(f"{Server.now()} -- sending ACK for packet {seq}")
                required_seq += 1
                break

            """# Receive data from the client
            packet_data = data[8:]  # Extract the data part of the packet
            if not packet_data:
                break
            print(f"Received data: {packet_data}")
            break"""

        

        """elif (fin == 1):  # Assuming 'fin' is a flag indicating a FIN packet
            print("FIN packet is received")
            # Send a response back to the client
            fin_ack = Packets.create_packet(0, 0, 4, 0, b'')
            serverSocket.sendto(fin_ack, clientAddress)
            print("FIN-ACK packet is sent")"""
        

        #After the establishment of the connection, we can send and receive data
        """while True:
            
            # Receive data from the client
            packet_data = data[8:]  # Extract the data part of the packet
            if not packet_data:
                break
			# Process the received data
            print(f"Received data: {packet_data}")
"""
    @staticmethod
    def main(serverIP, serverPort):
        serverSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
        serverSocket.bind((serverIP, serverPort))  # Bind to the specified IP and port

        while True:
            # Receive data and client address
            data, clientAddress = serverSocket.recvfrom(1000)

            # Start a new thread to handle the client
            thread.start_new_thread(Server.handleClient, (data, clientAddress, serverSocket))

if __name__ == "__main__":
    Server.main()