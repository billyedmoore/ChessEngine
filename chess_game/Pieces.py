from abc import ABC, abstractmethod, abstractclassmethod
import logging


class Piece(ABC):
    """
    Abstract class to be implemented by the individual piece type

    Properties:
        position - position of the piece on the board form (x:int, y:int)
        colour - colour of the piece, possible colours {"B","W"}
    Methods:
        get_legal_moves() - returns a list of legal moves
        move(move_to: tuple (int,int)) - moves the piece (does not verify that a move is legal)
    """
    _colour = None
    _position = (None, None)
    _moved = False

    @property
    def position(self) -> tuple:
        """
        The current position of the piece on the board in the form (x:int,y:int)
        """
        return self._position

    @position.setter
    def position_setter(self, position) -> None:
        """
        sets the position of a piece
        """
        if type(position) == tuple:
            if len(position) == 2:
                if type(position[0]) == int and type(position[1]) == int:
                    self._position = position
        logging.debug(f"Failed to set the position to {position}")

    @property
    def colour(self) -> str:
        """
        Representation of the color of the piece "B" for black pieces and "W"
        for white pieces
        """
        return self._position

    @colour.setter
    def colour_setter(self, colour) -> None:
        if colour.upper() in ["B", "W"]:
            self._colour = colour
        logging.debug(f"Failed to set the colour to {colour}")

    @abstractmethod
    def get_legal_moves(self):
        pass

    def make_move(self, move) -> None:
        pass


class Pawn(Piece):
    """
    Implementation of Piece class
    """

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        current_x = self.position[0]
        current_y = self.position[1]
        next_square = (current_x + 1, current_y)
        if game_state.square_exists(next_square) and game_state.square_is_empty(next_square):
            pass


