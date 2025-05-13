import argparse
from server import Server

def main():
    f = open("ronaldo.jpg", 'rb')
    data = f.read()
    f.close()

    # Print the first 100 bytes of the file
    print("First 100 bytes of the file:")
    for i in range(100):
        print(data[i], end=' ')
    print("\n")

    for line in data:
        print(line)


if __name__ == "__main__":
    main()