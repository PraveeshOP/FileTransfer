from socket import *
from packets import Packets
from datetime import datetime

class Server:
    
    @staticmethod
    def now():
        # Get the current time
        now = datetime.now()

        # Format the time to include hours, minutes, seconds, and microseconds
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond}"
        return formatted_time

    @staticmethod
    def main(serverIP, serverPort):
        serverSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
        serverSocket.bind((serverIP, serverPort))  # Bind to the specified IP and port

        #serverSocket.settimeout(1)  # Set a timeout for the socket operations

        try:
            required_seq = 1 # Initialize the expected sequence number
            totalfile = b"" # Initialize an empty byte string to store the received file data
            while True:

                packet, clientAddress = serverSocket.recvfrom(1000)  # Receive data from the client
                # Unpack the received packet_header
                packet_header = packet[:8]
                c_sequence_number, c_acknowledgment_number, c_flags, c_window = Packets.parse_header(packet_header)

                #packet data
                packet_data = packet[8:]  # Extract the data part of the packet
                
                # Check the flags to determine the type of packet received
                syn, ack, fin = Packets.parse_flags(c_flags)

                if (syn == 8):
                    print("SYN packet is received")
                    # Send a response back to the client
                    syn_ack = Packets.create_packet(0, 0, 12, 0, b'')
                    serverSocket.sendto(syn_ack, clientAddress)
                    print("SYN-ACK packet is sent")
                
                elif (ack == 4):
                    print("ACK packet is received")
                    print("Connection established\n")
                    first_packet_req = Packets.create_packet(0, 1, 0, 0, b'')
                    serverSocket.sendto(first_packet_req, clientAddress)

                elif (fin == 2):
                    print("\nFIN packet is received")
                    # Send a response back to the client
                    fin_ack = Packets.create_packet(0, 0, 6, 0, b'')
                    serverSocket.sendto(fin_ack, clientAddress)
                    print("FIN-ACK packet is sent")
                    break

                elif (c_sequence_number == required_seq):
                    totalfile += packet_data # Append the received data to the total file data
                    print(f"{Server.now()} -- packet {c_sequence_number} is received")
                    print(f"{Server.now()} -- sending ACK for packet {c_sequence_number}")
                    required_seq += 1
                    msg = Packets.create_packet(c_acknowledgment_number, required_seq, 0, 0, b'')
                    serverSocket.sendto(msg, clientAddress)
                    print("Requested packet ", required_seq)
                    continue
            
            print("Received file data:", totalfile.decode())

        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, shutting down the server.")

if __name__ == "__main__":
    Server.main()