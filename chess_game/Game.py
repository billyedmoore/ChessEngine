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
        white_checkmate = self.gamestate.checkmate("w")
        black_checkmate = self.gamestate.checkmate("b")
        if white_checkmate and not black_checkmate:
            return "w"
        elif black_checkmate and not white_checkmate:
            return "b"
        elif white_checkmate and black_checkmate:
            return "d"
        else:
            return ""


    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, gamestate):
        if type(gamestate) == GameState:
            self._gamestate = gamestate
        else:
            raise TypeError("Not of type GameState")

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
