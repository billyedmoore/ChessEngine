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
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                thing = bytes(json.dumps(request), "utf-8")
                s.sendall(thing)
                data = s.recv(1024)
                data = json.loads(data.decode("utf-8"))
                return (data)
        # json decode error is for when the server returns None due to an error
        except (json.decoder.JSONDecodeError, ConnectionError):
            print()
            self.app.open_connection_error_screen()
            return {}

    def login(self, username, password):
        request = {
            "type": "user",
            "request": "login",
            "username": username,
            "password": password
        }
        response = self._make_request(request)
        if not response or response.get("error"):
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

    def register(self, username, email, password_one, password_two):
        """
        Register a user with the server (calls create user route)
        """
        if password_one != password_two:
            return (False, "password")

        request = {
            "type": "user",
            "request": "create_user",
            "username": username,
            "email": email,
            "password": password_one
        }

        response = self._make_request(request)  # make request to server

        # bool only for clarity
        return (bool(response.get("created")), response.get("reason"))

    def join_game(self):
        auth_string = self.app.user.session_auth

        request = {
            "type": "game",
            "request": "join_game",
            "session_auth": auth_string
        }

        response = self._make_request(request)
        print("server responded ", response)
        game_id = response.get("game_id")
        colour = response.get("colour")

        while not game_id:
            response = self._make_request(request)
            game_id = response.get("game_id")
        print(game_id)

        return game_id, colour

    """
    Methods for OnlineGame class
    """

    def is_game_over(self, game_id):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "is_game_over",
            "game_id": game_id,
            "session_auth": session_auth,
        }
        response = self._make_request(request).get("is_game_over")

        return response

    def get_legal_moves(self):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_legal_moves",
            "session_auth": session_auth,
        }

        response = self._make_request(request).get("is_game_over")

    def get_previous_moves(self, colour):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_previous_moves",
            "session_auth": session_auth,
            "colour": colour
        }

        response = self._make_request(request).get("previous_moves")
        return response

    def get_one_colour_board(self, colour):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_one_colour_board",
            "session_auth": session_auth,
            "colour": colour
        }

        board = self._make_request(request).get("board")

        return board

    def possible_move_positions_for_piece(self, coord):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "possible_move_positions_for_piece",
            "session_auth": session_auth,
            "coord": coord
        }
        response = self._make_request(request).get("possible_positions")
        if not response:
            response == []
        return response

    def make_move(self, move):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "make_move",
            "session_auth": session_auth,
            "move": move
        }
        response = self._make_request(request).get("made_move")
        return response

    def get_player_to_play(self):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_player_to_play",
            "session_auth": session_auth
        }
        response = self._make_request(request).get("player_to_play")
        return response

    def get_algebraic_notation(self, pos_from, pos_to):
        session_auth = self.app.user.session_auth
        request = {
            "type": "game",
            "request": "get_algebraic_notation",
            "session_auth": session_auth,
            "pos_from": pos_from,
            "pos_to": pos_to
        }
        response = self._make_request(request)
        print(response)
        return response.get("algebraic_notation")
