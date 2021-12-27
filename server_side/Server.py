# server_side/Server.py
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
        self.games = {}
        self.inactive_games = {}
        self.matching_queue = []
        self.listening = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        while self.listening:
            conn, addr = self.server.accept()
            # print(f"Accepted connection from {addr}")
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
        return (colour.lower() in ["w", "b"])

    @staticmethod
    def get_random_string(length=10):
        """
        Get a random string made up of uppercase characters and letters
        """
        # Doesn't need to be in the class but it makes it easier
        return "".join(random.choice(
            string.digits + string.ascii_uppercase) for i in range(length))

    def _handle_request(self, request):
        print("Reuqest made", request)
        if request.get("type") == "game":
            # print("game request")
            response = self._handle_game_request(request)
        elif request.get("type") == "user":
            # print("user request")
            response = self._handle_user_request(request)

        print("Responded", response)
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
        valid_requests = ["login", "get_user", "create_user"]
        if request.get("request") == "login":
            return self._user_login_route(request)
        elif request.get("request") == "create_user":
            return self._create_user_route(request)
        elif not self._is_valid_auth_string(request.get("session_auth")):
            return {"error": "Invalid session_auth"}
        elif request.get("request") == "get_user":
            return self._get_user_route(request)
        else:
            return {"error": "Invalid user request"}

    def _create_user_route(self, request):
        """
        Route to create/register a user in the database.
        """
        # requests should contain the following arguments
        #       username
        #       email
        #       password

        username = request.get("username")
        email = request.get("email")
        password = request.get("password")

        is_valid, reason = User.is_valid_user(username, email, password)
        if not is_valid:
            return {"created": False, "reason": reason}

        created = User.create_user(username, email, password)
        if not created:
            return {"created": created, "reason": "exists"}
        else:
            return {"created": created}

    def _user_login_route(self, request):
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
                auth_string = Server.get_random_string()
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
            return valid_requests[req](request)

    def _is_valid_auth_string(self, string):
        """
        Is an auth string in the list of valid auth strings
        """
        return (string in self.users.keys())

    def _join_game_route(self, request):
        """
        Join the queue for joining a game or join one
        """
        game_id = self._get_current_game_id(request.get("session_auth"))
        if game_id:
            # dict comp to flip values and keys in game dict
            # find the key that coresponds to the users session auth
            # this is the colour they are playing as
            colour = {v: k for k, v in self.games[game_id].items()}.get(
                request.get("session_auth"))
            return {"error": f"Already in game {game_id}.", "game_id": game_id,
                    "colour": colour}
        elif len(self.matching_queue) == 0:
            self.matching_queue.append(request.get("session_auth"))
            return {"error": f"Waiting for a player to play."}
        elif request.get("session_auth") in self.matching_queue:
            return {"error": f"Waiting for a player to play."}
        else:
            game = Game(None, None)
            game_id = Server.get_random_string(length=5)
            index = len(self.games)
            print("new game", {"w": request.get("session_auth"),
                               "b": self.matching_queue[0],
                               "game": game,
                               "last_player": "b"})
            self.games[game_id] = ({"w": request.get("session_auth"),
                                    "b": self.matching_queue[0],
                                    "game": game,
                                    "game_over": "",
                                    "last_player": "b"})
            self.matching_queue.pop(0)
            return {"game_id": index, "colour": "w"}

    def _get_one_colour_board_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            colour = request.get("colour")
            if not self.is_valid_colour(colour):
                return {"error": "Invalid colour argument"}
            print(self.games[game_id])
            return {"board": self.games[game_id]["game"].get_one_colour_board(colour)}

    def _get_legal_moves_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            game = self.games[game_id]
            return {"legal_moves": game.get_legal_moves()}

    def _make_move_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            # gets the colour by session_auth
            colour_playing = list(self.games[game_id].keys(
            ))[list(self.games[game_id].values()).index(request.get("session_auth"))]
            if colour_playing.lower() != self.games[game_id]["game"].player_to_play.lower():
                return {"made_move": False}
            print(self.games[game_id])
            move = request.get("move")
            return {"made_move":
                    self.games[game_id]["game"].make_move(move, colour_playing=colour_playing)}
        print(f"made the move {move} or at least tryed ig")
        self.games[game_id]["game"].print()

    def _is_game_over_route(self, request):
        game_id_from_request = request.get("game_id")
        game_id = (game_id_from_request if
                   game_id_from_request else
                   self._get_current_game_id(request.get("session_auth")))
        all_games = {**self.games,
                     **self.inactive_games}
        valid_game_ids = [k for k in all_games.keys()]
        if game_id not in valid_game_ids:
            return {"error": "User not in a game."}
        else:
            current_game_over_state = all_games[game_id].get(
                "game_over")
            if current_game_over_state:
                return {"is_game_over": current_game_over_state}
            else:
                current_game_over_state = all_games[game_id]["game"].is_game_over
                if current_game_over_state:
                    self.games[game_id]["game_over"] = current_game_over_state
                    self._handle_game_over(game_id, "w")
                    return {"is_game_over": current_game_over_state}
                else:
                    return {"is_game_over": False}

    def _handle_game_over(self, game_id, game_over_code):
        """
        Called when a game first returns a affermative value to a
        "is_game_over" request. Basically when the server class becomes aware
        a game is over.
        """

        # information about the game in the self.games dir
        game_dict = self.games[game_id]

        white_user = self.users[game_dict["w"]]
        black_user = self.users[game_dict["b"]]

        if game_over_code == "w":
            new_white_elo, new_black_elo = self.calculate_elo(
                white_user.elo, black_user.elo)
        elif game_over_code == "b":
            new_black_elo, new_white_elo = self.calculate_elo(
                black_user.elo, white_user.elo)
        else:
            new_black_elo = black_user.elo
            new_white_elo = white_user.elo

        # set the elos of the users objects, this will also change val in the
        # database
        white_user.elo = (new_white_elo)
        black_user.elo = (new_black_elo)

        # remove game from the self.games dict
        # Personal Note - Not a fan of the del keyword and would rather user a
        #                 function to do this but couldn't think of one
        del self.games[game_id]
        # add game to the inactive_games_dict
        self.inactive_games[game_id] = game_dict

    @ staticmethod
    def calculate_elo(winning_elo, losing_elo):
        k = 40  # this is the sensitivity of the elo rating
        expected_score = (1/(1+10**((losing_elo-winning_elo)//400)))
        new_winning_elo = int(winning_elo + k*(1-expected_score))
        new_losing_elo = int(losing_elo + k*(0-expected_score))
        return new_winning_elo, new_losing_elo

    def _get_player_to_play_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            return {"player_to_play": self.games[game_id]["game"].player_to_play}

    def _tick_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            self.games[game_id]["game"].tick()
            return {}

    def _possible_move_positions_from_piece_route(self, request):
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            coord = request.get("coord")
            return {"possible_positions": self.games[game_id]["game"].possible_move_positions_for_piece(coord)}

    def _get_current_game_id(self, auth_string):
        for game_id, game in self.games.items():
            players_in_game = [game["w"], game["b"]]
            if auth_string in players_in_game:
                return game_id
        else:
            return None

    def _get_current_game_id_route(self, request):
        """
        Serve the current game_id of a user in a json object
        """
        session_auth = request.get("session_auth")
        game_id = self._get_current_game_id(session_auth)
        if not game_id:
            return {"game_id": game_id}
        else:
            return {"error": "User not in a game."}

    def _get_previous_moves_route(self, request):
        """
        Serve the current game_id of a user in a json object
        """
        session_auth = request.get("session_auth")
        game_id = self._get_current_game_id(session_auth)
        if not game_id:
            return {"error": "User not in a game."}
        else:
            colour = request.get("colour")
            return {"previous_moves": self.games[game_id]["game"].get_previous_moves(colour)}

    def _get_algebraic_notation_route(self, request):
        print("geting algebraic_notation")
        game_id = self._get_current_game_id(request.get("session_auth"))
        if not game_id:
            return {"error": "User not in a game."}
        else:
            pos_from = request.get("pos_from")
            pos_to = request.get("pos_to")
            # print({"algebraic_notation": self.games[game_id]["game"].get_algebraic_notation(
            # pos_from, pos_to)})
            if self.games[game_id]["game"].get_algebraic_notation(pos_from, pos_to):
                return {"algebraic_notation": self.games[game_id]["game"].get_algebraic_notation(pos_from, pos_to)}
            else:
                return {"error": "invalid move"}
