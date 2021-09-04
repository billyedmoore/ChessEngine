import socket
import json
import sys


HOST = "127.0.0.1"
PORT = 65432
try:
    username = sys.argv[1]
except KeyError:
    username = "billyedmoore"
requests = {
    "login": {
        "type": "user",
        "request": "login",
        "username": username,
        "password": "password"
    },
    "join_game": {
        "type": "game",
        "request": "join_game"
    },
    "get_game_id": {
        "type": "game",
        "request": "get_current_game_id"
    }}


def send_request(request, session_auth=""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request["session_auth"] = session_auth
        thing = bytes(json.dumps(request), "utf-8")
        s.sendall(thing)
        data = s.recv(1024)
        data = json.loads(data.decode("utf-8"))
        if data.get("session_auth"):
            return (data.get("session_auth"), data)
        else:
            return (session_auth, data)


order_of_operations = ["login", "join_game", "get_game_id"]

session_auth = ""
for order in order_of_operations:
    session_auth, data = send_request(
        requests[order], session_auth=session_auth)
    print(data)
