import socket
import json


class Client():
    """
    Makes requests to the Server on behalf of the front end app.
    """

    def __init__(self, app, host, port):
        # session auth should be stored in app.session_auth after login
        self.app = app
        self.host = host
        self.port = port

    def _make_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            thing = bytes(json.dumps(request), "utf-8")
            s.sendall(thing)
            data = s.recv(1024)
            data = json.loads(data.decode("utf-8"))
            return (data)

    def login(self, username, password):
        request = {
            "type": "user",
            "request": "login",
            "username": username,
            "password": password
        }
        response = self._make_request(request)
        if response.get("error"):
            return {}
        session_auth = response.get("session_auth")
        request = {
            "type": "user",
            "request": "get_user",
            "session_auth": session_auth
        }
        user = self._make_request(request)
        user["session_auth"] = session_auth
        return user

    def join_game(self, username, password):
        auth_string = self.app.user.session_auth

        request = {
            "type": "game",
            "request": "join_game",
            "session_auth": auth_string
        }
        get_game_id_request = {
            "type": "game",
            "request": "get_game_id",
            "session_auth": auth_string}

        response = self._make_request(request)
        game_id = response.get("game_id")

        while not game_id:
            response = self._make_request(request)
            game_id = response.get("game_id")

        return game_id

    def get_one_colour_board(self, colour):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_one_colour_board",
            "session_auth": session_auth,
            "colour": colour
        }

        board = self._make_request(request)

        return board

    def make_move(self):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "make_move",
            "session_auth": session_auth,
            "move": "move"
        }
        response = self._make_request(request)
        return response
