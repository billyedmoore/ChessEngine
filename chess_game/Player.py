from .GameState import GameState
from .Move import BaseMove


class BasePlayer:
    """
    Base class for players, to be inherited by AIPlayer and Player
    """
    _colour = ""
    _gamestate = None

    def __init__(self, colour):
        self.colour = colour

    @property
    def colour(self):
        return self._colour.lower()

    @colour.setter
    def colour(self, colour):
        colour = colour.lower()
        if colour in ["w", "b"]:
            self._colour = colour

    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, gamestate):
        if type(gamestate) == GameState:
            self._gamestate = gamestate
        else:
            raise TypeError("Not of type GameState")

    def get_next_move(self) -> BaseMove:
        pass


class TerminalPlayer(BasePlayer):
    """
    Class for a terminal player (Not to be used in prod only as placeholder
    prior to building out frontend)
    """

    def __init__(self, colour):
        super().__init__(colour)

    def get_next_move(self):
        print(f"{'white' if self.colour =='w' else 'black'} enter your move: ")
        move = None
        while not move:
            algebraic_move = input("move :")
            move = BaseMove.from_algebraic_notation(
                self.gamestate,  self.colour, algebraic_move)
        return move
