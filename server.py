from socket import *
from packets import Packets
from datetime import datetime
import sys

class Server:
    
    @staticmethod
    def now():
        # Get the current time
        now = datetime.now()

        # Format the time to include hours, minutes, seconds, and microseconds
        formatted_time = now.strftime("%H:%M:%S") + f".{now.microsecond}"
        return formatted_time

    @staticmethod
    def main(serverIP, serverPort, discard_packet):
        try:
            serverSocket = socket(AF_INET, SOCK_DGRAM)
            serverSocket.bind((serverIP, serverPort))

            required_seq = 1  # Expected sequence number
            totalfile = b""  # Buffer to store received file data
            serverWindow = 15  # Server's advertised window size
            start_time = None  # Start time for throughput calculation
            total_data_received = 0  # Total data received in bytes

            while True:
                packet, clientAddress = serverSocket.recvfrom(1000)
                packet_header = packet[:8]
                c_sequence_number, c_acknowledgment_number, c_flags, c_window = Packets.parse_header(packet_header)
                packet_data = packet[8:]  # Extract data from the packet

                # Parse flags
                syn, ack, fin = Packets.parse_flags(c_flags)

                if (syn == 8):  # SYN packet received
                    print("SYN packet is received")
                    syn_ack = Packets.create_packet(0, 0, 12, serverWindow, b'')
                    serverSocket.sendto(syn_ack, clientAddress)
                    print("SYN-ACK packet is sent")

                elif (ack == 4 and c_sequence_number == 0):  # ACK for SYN-ACK
                    print("ACK packet is received")
                    print("Connection established\n")
                    start_time = datetime.now()  # Start the timer for throughput calculation

                elif (fin == 2):  # FIN packet received
                    print("\nFIN packet is received")
                    fin_ack = Packets.create_packet(0, 0, 6, 0, b'')
                    serverSocket.sendto(fin_ack, clientAddress)
                    print("FIN-ACK packet is sent")
                    break

                elif (c_sequence_number == required_seq):  # Correct packet received
                    if (c_sequence_number == discard_packet):
                        discard_packet -= 1
                    else:
                        totalfile += packet_data
                        total_data_received += len(packet_data)
                        print(f"{Server.now()} -- packet {c_sequence_number} is received")
                        print(f"{Server.now()} -- sending ack for the received {c_sequence_number}")
                        ack_packet = Packets.create_packet(0, required_seq, 4, serverWindow, b'')
                        serverSocket.sendto(ack_packet, clientAddress)
                        print(f"ack which is sent is {required_seq}")
                        required_seq += 1

                else:  # Out-of-order or duplicate packet
                    print(f"{Server.now()} -- out-of-order or duplicate packet {c_sequence_number} is received")
                    # Resending ACK for the last correctly received packet
                    ack_packet = Packets.create_packet(0, required_seq-1, 4, serverWindow, b'')
                    serverSocket.sendto(ack_packet, clientAddress)

            # Write the received file to disk
            with open("output_image.jpg", "wb") as output_file:
                output_file.write(totalfile)

            # Calculate throughput
            end_time = datetime.now()
            run_time = (end_time - start_time).total_seconds()
            throughput = (total_data_received * 8) / (run_time * 1_000_000)  # Mbps
            print(f"\nThe throughput is {throughput:.2f} Mbps")
            print("Connection Closes\n")

        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, shutting down the server.")
            sys.exit()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()
        except timeout:
            sys.exit()
        finally:
            serverSocket.close()
            sys.exit()
