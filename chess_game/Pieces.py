class Piece:
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
    _letter = "F"

    def __init__(self, position, color):
        self._position = position
        self._colour = color

    @property
    def letter(self) -> str:
        if self.colour.lower() == "w":
            return self._letter.lower()
        if self.colour.lower() == "b":
            return self._letter.upper()
        # TODO raise exception if color isn't a valid value

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
        return self._colour

    @colour.setter
    def colour_setter(self, colour) -> None:
        if colour.upper() in ["B", "W"]:
            self._colour = colour.upper()

    def get_legal_moves(self):
        pass

    @colour.setter
    def colour(self, value):
        self._colour = value


class Pawn(Piece):
    """
    Implementation of Piece class
    """

    _letter = "P"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None


class Bishop(Piece):
    """
    Implementation of Piece class
    """

    _letter = "B"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None


class Queen(Piece):
    """
    Implementation of Piece class
    """

    _letter = "Q"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None


class King(Piece):
    """
    Implementation of Piece class
    """

    _letter = "K"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None


class Rook(Piece):
    """
    Implementation of Piece class
    """

    _letter = "R"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None


class Knight(Piece):
    """
    Implementation of Piece class
    """

    _letter = "N"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_legal_moves(self, game_state):
        return None
