import socket
import json
from .User import User
import random
import string


class Server():
    """
    Server to handle requests from the client, this will allow for online games
    handing users and global rankings.

    Requests should be in the format:
        {
            "type" : ["game" or "user"],
            "session_auth" : "string" (not allways required),
            "request" : "request" (like a function name),
            arrgs* : any arrgs required by the function
        }

    Methods:
        None Server()  : constructor
    """

    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.users = {}
        self.games = {}
        self.listening = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        while self.listening:
            conn, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            request = conn.recv(4096)
            if not request:
                break
            request = self.bytes_to_json(request)
            if type(request) != dict:
                response = "Please provide your request as a json object (python dict)"
            if request.get("type") == "game":
                response = self._handle_game_request(request)
            elif request.get("type") == "user":
                response = self._handle_user_request(request)

            conn.send(json.dumps(response).encode("utf-8"))
            conn.close()
        self.server.close()

    @staticmethod
    def bytes_to_json(data):
        """
        Convert a encoded string to a data structure so that it can be properly
        handled.

        Parameters:
            bytes data - utf-8 encoded json string
        """
        data = data.decode("utf-8")
        return json.loads(data)

    def _handle_user_request(self, request):
        """
        Valid user requests:
            login - returns a string session auth string
                username - the username
                password - the unhashed password

        """
        def get_random_string(length=10):
            return "".join(random.choice(
                string.digits+string.ascii_uppercase) for i in range(length))
        valid_requests = ["login"]
        if request.get("request") not in valid_requests:
            return {"error": "Invalid user request"}
        elif request.get("request") == "login":
            user = User.get_user(request.get("username"),
                                 request.get("password"))
            if user:
                # TODO check that the user is not allready logged in
                auth_string = get_random_string()
                while auth_string in self.users.keys():
                    auth_string = get_random_string()
                self.users[auth_string] = user
                return {"session_auth": auth_string}
            else:
                return {"error": "Invalid username or password"}

    def _handle_game_request(self, request):
        valid_requests = []
        if request.get("request") not in valid_requests:
            return {"error": "Invalid user request"}
