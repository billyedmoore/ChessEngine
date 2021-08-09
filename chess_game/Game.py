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

    def print(self):
        self._gamestate.print()

    def play_next_move(self):
        player = self._white_player if self._gamestate.player_to_play.lower(
        ) == "w" else self._black_player
        move = player.get_next_move()
        self._gamestate.make_move(move)
