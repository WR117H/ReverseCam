import cv2
import socket
import pickle
import struct


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'  # Replace with the server IP address
port = 9999

# Connect to the server
client_socket.connect((host_ip, port))

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Serialize the frame using pickle
    data = pickle.dumps(frame)

    # Pack the serialized frame and its length into a struct
    message = struct.pack("Q", len(data)) + data

    # Send the frame to the server
    client_socket.sendall(message)

    # Break the loop if 'Enter' is pressed
    if cv2.waitKey(1) == 13:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
client_socket.close()
