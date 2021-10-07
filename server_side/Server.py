import socket
from chess_game.Game import Game
import json
from .User import User
import random
import string


class Server():
    """
    Server to handle requests from the client, this will allow for online games
    handing users and global rankings. Extra arguments in json objects will be
    ignored without error.

    Requests should be in the format:
        {
            "type" : ["game" or "user"],
            "session_auth" : "string" (not allways required),
            "request" : "request" (like a function name),
            args* : any args required by the function
        }

    Methods:
        None Server()  : constructor
    """

    def __init__(self, host="127.0.0.1", port=65432):
        self.host = host
        self.port = port
        self.users = {}
        self.games = []
        self.matching_queue = []
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
            response = self._handle_request(request)
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

    @staticmethod
    def is_valid_colour(colour):
        return (colour.lower() in ["w", "l"])

    def _handle_request(self, request):
        print(request)
        if request.get("type") == "game":
            print("game request")
            response = self._handle_game_request(request)
        elif request.get("type") == "user":
            print("user request")
            response = self._handle_user_request(request)

        return response

    def _handle_user_request(self, request):
        """
        Valid user requests:
            login - returns a string session auth string
                parameters:
                    username - the username
                    password - the unhashed password
                returns:
                    session_auth - string to be used to authenicate users
        """
        valid_requests = ["login", "get_user"]
        if request.get("request") not in valid_requests:
            return {"error": "Invalid user request"}
        if request.get("request") == "login":
            return self._user_login_route(request)
        if not self._is_valid_auth_string(request.get("session_auth")):
            return {"error": "Invalid session_auth"}
        if request.get("request") == "get_user":
            return self._get_user_route(request)

    def _user_login_route(self, request):
        def get_random_string(length=10):
            return "".join(random.choice(
                string.digits + string.ascii_uppercase) for i in range(length))

        user = User.get_user(request.get("username"),
                             request.get("password"))
        if user:

            # if user allready logged in
            if user.username in [u.username for u in self.users.values()]:
                # get the user from self.users
                user = [u for u in self.users.values() if u.username ==
                        user.username][0]
                # get the auth_string that is associated with that user
                auth_string = [
                    k for k, v in self.users.items() if v == user][0]
                return {"session_auth": auth_string}

            # if user is not yet logged in
            else:
                auth_string = get_random_string()
                while auth_string in self.users.keys():
                    auth_string = get_random_string()
                self.users[auth_string] = user
                return {"session_auth": auth_string}
        else:
            return {"error": "Invalid username or password"}

    def _get_user_route(self, request):
        """
        Get details of the user currently logged in
        """
        user = self.users[request.get("session_auth")]
        print(type(user.elo))
        response = {"user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "elo": user.elo}
        return response

    def _handle_game_request(self, request):
        """
        Valid user requests:
            join_game - adds a to the waiting list for games or adds to a game
                        if more than one is allready waiting
                parameters:
                    session_auth - a string provided when a user logs in
                returns:
                    game_id - ONLY RETURNED IF ADDED TO GAME
            get_current_game_id - gets the id of the game
        """
        valid_requests = {"join_game": self._join_game_route,
                          "get_current_game_id": self._get_current_game_id_route,
                          "get_one_colour_board": self._get_one_colour_board_route,
                          "make_move": self._make_move_route,
                          "get_legal_moves": self._get_legal_moves_route,
                          "get_previous_moves": self._get_previous_moves_route,
                          "is_game_over": self._is_game_over_route,
                          "get_player_to_play": self._get_player_to_play_route,
                          "possible_move_positions_for_piece": self._possible_move_positions_from_piece_route,
                          "get_algebraic_notation": self._get_algebraic_notation_route}

        req = request.get("request")
        if req not in valid_requests.keys():
            return {"error": "Invalid game request"}
        elif not self._is_valid_auth_string(request.get("session_auth")):
            return {"error": "User not authenticated"}
        else:
            valid_requests[req](request)

    def _is_valid_auth_string(self, string):
        return (string in self.users.keys())

    def _join_game_route(self, request):
        """
        Join the queue for joining a game or join one
        """
        game_id = self._get_current_game_id(request.get("session_auth"))
        if game_id in range(len(self.games)):
            return {"error": f"Already in game {game_id}"}
        elif len(self.matching_queue) == 0:
            self.matching_queue.append(request.get("session_auth"))
            return {}
        else:
            game = Game(None, None)
            index = len(self.games)
            self.games.append({"w": request.get("session_auth"),
                               "b": self.matching_queue[0],
                               "game": game,
                               "last_player":"b"})
            self.matching_queue.pop(0)
            return {"game_id": index}

    def _get_one_colour_board_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            colour = request.get("colour")
            if not self.is_valid_colour(colour):
                return {"error": "Invalid colour argument"}
            return {"board": self.games[game_id]["game"].get_one_colour_board(colour)}

    def _get_legal_moves_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            game = self.games[game_id]
            return {"legal_moves": game.get_legal_moves()}

    def _make_move_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            move = request.get("move")
            return {"made_move": self.games[game_id]["game"].make_move(move)}

    def _is_game_over_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            return {"is_game_over": self.games[game_id]["game"].is_game_over}

    def _get_player_to_play_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            return {"player_to_play": self.games[game_id]["game"].player_to_play}

    def _tick_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            self.games[game_id]["game"].tick()
            return {}

    def _possible_move_positions_from_piece_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            coord = request.get("coord")
            return {"possible_positions": self.games[game_id]["game"].possible_move_positions_from_piece(coord)}

    def _get_current_game_id(self, auth_string):
        for game in self.games:
            players_in_game = [game["w"], game["b"]]
            if auth_string in players_in_game:
                return self.games.index(game)
        else:
            return None

    def _get_current_game_id_route(self, request):
        """
        Serve the current game_id of a user in a json object
        """
        session_auth = request.get("session_auth")
        game_id = self._get_current_game_id(session_auth)
        if type(game_id) == int:
            return {"game_id": game_id}
        else:
            return {"error": "User not in a game."}

    def _get_previous_moves_route(self, request):
        """
        Serve the current game_id of a user in a json object
        """
        session_auth = request.get("session_auth")
        game_id = self._get_current_game_id(session_auth)
        if type(game_id) == int:
            return {"error": "User not in a game."}
        else:
            colour = request.get("colour")
            return {"previous_moves": self.games[game_id]["game"].get_previous_moves(colour)}

    def _get_algebraic_notation_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if type(game_id) != int:
            return {"error": "User not in a game."}
        else:
            pos_from = request.get("pos_from")
            pos_to = request.get("pos_to")
            return {"algebraic_notation": self.games[game_id]["game"].get_algebraic_notation(pos_from, pos_to)}
