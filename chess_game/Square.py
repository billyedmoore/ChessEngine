class Square:
    """
    A class to represent one square on a chess board

    Properties:
        position - position of the square on the board form (x:int, y:int) (no setter)
    Methods:
        Square(position : tuple(int, int))
        pop_piece() - returns the piece located on the square and set current piece to None
        set_piece(piece : Piece) - sets the current piece to the piece passed in
        is_empty() - returns True when _piece = None
    """
    _position = None
    _piece = None

    def __init__(self, position):
        self._position = position

    @property
    def position(self):
        """
        The position of the square of the board denoted by a tuple : (x :int,y :int)
        """
        return self._position

    @position.setter
    def position(self, pos, game):
        if game.square_exists(pos) and game.square_is_empty(pos):
            self._position = pos
        else:
            raise Exception("Invalid board position.")
            # TODO: make a relevant exception so it can be caught without catching all errors

    def pop_piece(self):
        """
        Return the current piece and set the current piece value to None
        Ensures that only one version of the piece exists
        """
        p = self._piece
        p.position = (None, None)
        self._piece = None
        return p

    def get_piece(self):
        """
        Returns the current piece without setting the piece attribute to None
        Essentially makes a copy of the Piece
        """
        return self._piece

    def set_piece(self, piece):
        """
        Sets the current piece, this will only work when the piece is currently null
        """
        if not self._piece:
            self._piece = piece
            self._piece.position = self.position
        else:
            raise Exception(f"Pop or Remove piece before setting a new one.")
            # TODO: make a relevant exception so it can be caught without catching all errors

    def is_empty(self):
        return not bool(self._piece)
