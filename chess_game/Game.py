from .GameState import GameState
from .Move import Move, PromotionMove


class Game:
    """
    Class for a game of chess
    """
    _gamestate = None  # of type GameState
    _white_player = None  # of type Player or None
    _black_player = None  # of type Player or None

    def __init__(self, white_player, black_player, 
            fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self._gamestate = GameState(fen_string=fen_string)
        if white_player:
            white_player.gamestate = self._gamestate
        if black_player:
            black_player.gamestate = self._gamestate
        self._white_player = white_player
        self._black_player = black_player

    @property
    def is_game_over(self):
        """
        Returns a string describing the outcome of the game if game over.

        Possible Return Values:
            "b" - black wins
            "w" - white wins
            "d" - draw
            ""  - game is not over
        """
        # Other ways that the game can be over:
        # Threefold repetition - position repeated three times in a game
        # 50 move rule - no captures or pawn moves made in last 50 moves
        stalemate = self.gamestate.stalemate()
        if stalemate:
            return "d"
        white_checkmate = self.gamestate.checkmate("w")
        black_checkmate = self.gamestate.checkmate("b")
        if white_checkmate and not black_checkmate:
            return "b"
        elif black_checkmate and not white_checkmate:
            return "w"
        elif white_checkmate and black_checkmate:
            return "d"
        else:
            return ""
    
    @property
    def black_player(self):
        return self._black_player

    @property
    def white_player(self):
        return self._white_player

    @property 
    def gamestate(self): 
        return self._gamestate

    @property
    def player_to_play(self):
        return self.gamestate.player_to_play

    @gamestate.setter
    def gamestate(self, gamestate: GameState):
        if type(gamestate) == GameState:
            self._gamestate = gamestate
            self._gamestate.moves.empty()
        else:
            raise TypeError("Not of type GameState")

    def get_legal_moves(self):
        """
        Returns a list of legal moves .

        Parameters
        """
        moves = self.gamestate.get_legal_moves(self.player_to_play)
        move_strings = [move.to_algebraic_notation() for move in moves]
        return move_strings

    def possible_move_positions_for_piece(self, coord):
        moves = [Move.from_algebraic_notation(
            self.gamestate, self.player_to_play, move) for move in self.get_legal_moves()]
        moves = [move for move in moves if (move.normal or
                                            move.promotion) and move.position_from == coord]
        return [move.position_to for move in moves]

    def get_previous_moves(self, colour: str):
        """
        Returns a list of previous moves in algebraic notation for a given colour.

        Parameters
            str colour - value from the set {"w","W","b","B"}
        """
        moves = self.gamestate.moves.get_moves()
        if colour.lower() == "w":
            return [moves[i].to_algebraic_notation() for i in range(len(moves)) if i % 2 == 0]

        elif colour.lower() == "b":
            return [moves[i].to_algebraic_notation() for i in range(len(moves)) if i % 2 == 1]

    def get_one_colour_board(self, colour):
        """
        Returns a repersentaion of the chess board only contating pieces of a
        specified colour.

        Parameters
            str colour - value from the set {"w","W","b","B"}
        """
        board = [square.get_piece() for square in self.gamestate._squares]
        board = [(piece.letter, piece.number) if piece and piece.colour.upper(
        ) == colour.upper() else "" for piece in board]
        board = [board[x:x+8] for x in range(0, len(board), 8)]
        return board

    def print(self):
        self._gamestate.print()

    def tick(self):
        # if no player is set moves should be made explicitly with the make move
        # method
        players = {"w": self._white_player, "b": self._black_player}
        player_to_play = players[self._gamestate.player_to_play.lower()]
        if player_to_play:
            move = player_to_play.get_next_move()
            self._gamestate.make_move(move)

    def make_move(self, algebraic_move, colour_playing=None):
        if not colour_playing or colour_playing.lower() not in ["w", "b"]:
            colour_playing = self.gamestate.player_to_play
        move = Move.from_algebraic_notation(
            self.gamestate, colour_playing, algebraic_move)
        if move:
            self.gamestate.make_move(move)
            return True
        self.gamestate.print()
        return False

    def get_algebraic_notation(self, pos_from, pos_to):
        special_moves = {"b": {((4, 0), (7, 0)): "O-O", ((4, 0), (0, 0)): "O-O-O"},
                         "w": {((4, 7), (7, 7)): "O-O", ((4, 7), (0, 7)): "O-O-O"}}

        colour_info = {
            "B": {"start_row": 1, "end_row": 7, "direction": +1},
            "W": {"start_row": 6, "end_row": 0, "direction": -1}}
        info = colour_info[self.player_to_play.upper()]
        special_moves = special_moves[self.player_to_play.lower()]
        try:
            print(tuple(pos_from), tuple(pos_to))
            move = special_moves[(tuple(pos_from), tuple(pos_to))]
            return move
        except KeyError as e:
            pass
        piece = self._gamestate.get_square(pos_from).get_piece()
        if piece:
            piece_letter = piece.letter
        else:
            return None

        if pos_to[1] == info["end_row"] and piece_letter.upper() == "P":
            move = PromotionMove(self.gamestate, pos_from, pos_to)
        else:
            move = Move(self.gamestate, pos_from, pos_to)

        return move.to_algebraic_notation()
