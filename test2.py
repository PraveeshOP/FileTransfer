from packets import Packets

def main():

    total_msg = b''
    # Open the file and ensure it is closed properly using a context manager
    with open("file.txt", "rb") as file:
        sequence_number = 1  # Initialize the sequence number
        while True:
            # Read 10 bytes of data from the file
            data = file.read(10)
            if not data:  # Break the loop if no more data is available
                break

            # Create a packet with the data
            acknowledgment_number = 0
            window = 0
            flags = 0
            # msg now holds a packet, including our custom header and data
            msg = Packets.create_packet(sequence_number, acknowledgment_number, flags, window, data)

            print("Packed data:", data)

            total_msg += msg

            # Print the data and increment the sequence number
            sequence_number += 1  # Increment the sequence number for the next packet

        #After the loop
        print("Printing the innhold", msg)

        #decoding the packet
        header_from_msg = msg[8:]
        message = total_msg.decode()
        print("Decoded message:", message)

if __name__ == "__main__":
    main()