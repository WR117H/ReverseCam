import cv2
import socket
import pickle
import struct
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('--ip', type=str, help='Server IP address')
parser.add_argument('--port', type=int, help='Server port number')
args = parser.parse_args()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_socket.bind((args.ip, args.port))

# Listen for incoming connections
server_socket.listen(5)

print("Waiting for a client to connect...")

# Accept a client connection
client_socket, addr = server_socket.accept()
print('Connected to:', addr)

# Initialize a variable to store the received frame
data = b""
payload_size = struct.calcsize("Q")

while True:
    # Receive data from the client
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # Adjust the buffer size as needed
        if not packet:
            break
        data += packet

    # Extract the length of the serialized frame from the received data
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    # Keep receiving data until the entire frame is received
    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)  # Adjust the buffer size as needed

    # Deserialize the received frame using pickle
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)

    # Display the received frame
    cv2.imshow('Server - Receiving Webcam', frame)
    if cv2.waitKey(1) == 13:  # Press 'Enter' to exit
        break

# Release resources
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()
