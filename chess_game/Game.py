from .GameState import GameState


class Game:
    """
    Class for a game of chess
    """
    _gamestate = None  # of type GameState
    _white_player = None  # of type Player
    _black_player = None  # of type Player

    def __init__(self, white_player, black_player, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self._gamestate = GameState(fen_string=fen_string)
        white_player.gamestate = self._gamestate
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
            "d" - nobody wins
            ""  - game is not over
        """
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
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, gamestate: GameState):
        if type(gamestate) == GameState:
            self._gamestate = gamestate
        else:
            raise TypeError("Not of type GameState")

    def get_legal_moves(self, colour: str):
        """
        Returns a list of legal moves in algebraic notation for a given colour.

        Parameters
            str colour - value from the set {"w","W","b","B"}
        """
        moves = self.gamestate.get_legal_moves()
        move_strings = [move.to_algebraic_notation() for move in moves]
        return move_strings

    def get_one_colour_board(self, colour):
        """
        Returns a repersentaion of the chess board only contating pieces of a 
        specified colour.

        Parameters
            str colour - value from the set {"w","W","b","B"}
        """
        board = [square.get_piece() for square in self.gamestate._squares]
        board = [piece for piece in board if not piece or piece.colour.upper()
                 == colour.upper()]
        board = [piece.letter if piece else "" for piece in board]
        board = [board[x:x+8] for x in range(0, len(board), 8)]
        print(board)
        return board

    def print(self):
        self._gamestate.print()

    def play_next_move(self):
        if self.is_game_over:
            if self.is_game_over == "w":
                print("White wins")
                return
            elif self.is_game_over == "b":
                print("Black wins")
                return
            elif self.is_game_over == "d":
                print("Draw")
                return
        player = self._white_player if self._gamestate.player_to_play.lower(
        ) == "w" else self._black_player
        move = player.get_next_move()
        self._gamestate.make_move(move)
