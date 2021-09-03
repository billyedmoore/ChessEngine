import socket
import json

HOST = "127.0.0.1"
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    thing = bytes(json.dumps({
        "type": "user",
        "request": "login",
        "username": "billyedmoore",
        "password": "password"
    }), "utf-8")
    s.sendall(thing)
    data = s.recv(1024)
    print(data)
