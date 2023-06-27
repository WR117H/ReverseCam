import cv2
import socket
import pickle
import struct
import argparse

# Addresses
ip_address = 'localhost'
port = 9999

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((ip_address, port))


# Open the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()

    # Serialize the frame using pickle
    frame_data = pickle.dumps(frame)

    # Get the size of the serialized frame
    msg_size = struct.pack("Q", len(frame_data))

    # Send the size of the serialized frame to the server
    client_socket.sendall(msg_size)

    # Send the serialized frame to the server
    client_socket.sendall(frame_data)

    # Display the sent frame

    if cv2.waitKey(1) == 13:  # Press 'Enter' to exit
        break

# Release resources
cv2.destroyAllWindows()
video_capture.release()
client_socket.close()
