# ReverseCam

![Screenshot 2023-06-16 143859](https://github.com/WR117H/ReverseCam/assets/97615989/c6e4c350-0a19-4c80-9d54-e851cfd16e1b)

A tool for gathering webcam's frames with reverse socket connection
# Setup
First install Reverse cam using git
```
git clone https://github.com/WR117H/ReverseCam.git
```
Then head to the folder
```
cd ReverseCam
```
Install the requirements using pip
```
pip install -r requirements.txt
```
Change the client's file addresses to whatever you want . . .

# Server useage
| Argument | Useage |
| --- | --- |
| `--ip` | Enter the server's ip address |
| `--port` | Enter the server's port of ip address |

# Examples
Server:
```
python server.py --ip 127.0.0.1 --port 9999
```
Client:
```
python client.py
```
