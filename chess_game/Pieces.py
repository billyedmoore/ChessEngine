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
    def position(self) -> tuple[int, int]:
        """
        The current position of the piece on the board in the form (x:int,y:int)
        """
        return self._position

    @position.setter
    def position_setter(self, position) -> None:
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
    def get_legal_moves(self) -> list[tuple[int, int]]:
        pass

    @abstractmethod
    def make_move(self, move) -> None:
        pass
