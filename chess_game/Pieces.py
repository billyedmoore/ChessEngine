from abc import ABC, abstractmethod, abstractclassmethod


class Piece(ABC):
    """
    Abstract class to be implemented by the individual piece type

    Properties:
        position - position of the piece on the board form (x:int, y:int)
        colour - colour of the piece, possible colours {"B","W"}
    Methods:
        get_legal_moves() - returns a list of legal moves
    """
    _colour = None
    _position = (None, None)
    _moved = False
    letter = "F"

    @property
    def position(self) -> tuple:
        """
        The current position of the piece on the board in the form (x:int,y:int)
        """
        return self._position

    @position.setter
    def position_setter(self, position) -> None:
        """
        sets the position of the piece
        """
        if type(position) == tuple:
            if len(position) == 2:
                if type(position[0]) == int and type(position[1]) == int:
                    self._position = position

    # TODO: raise an exception if the position isn't valid

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

    @abstractmethod
    def get_legal_moves(self):
        pass


class Pawn(Piece):
    """
    Implementation of Piece class
    """

    letter = "P"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None


class Bishop(Piece):
    """
    Implementation of Piece class
    """

    letter = "B"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None


class Queen(Piece):
    """
    Implementation of Piece class
    """

    letter = "Q"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None


class King(Piece):
    """
    Implementation of Piece class
    """

    letter = "K"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None


class Rook(Piece):
    """
    Implementation of Piece class
    """

    letter = "R"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None


class Knight(Piece):
    """
    Implementation of Piece class
    """

    letter = "N"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position):
        self.position = position

    def get_legal_moves(self, game_state):
        return None
