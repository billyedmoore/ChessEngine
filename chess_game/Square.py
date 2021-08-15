from .Move import Move, PromotionMove


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

    def __init__(self, gamestate, position):
        self._position = position
        self._gamestate = gamestate

    def clone(self, gamestate_clone):
        clone = Square(gamestate_clone, self.position)
        if self._piece:
            piece_cpy = self._piece.clone()
            clone.set_piece(piece_cpy)
        return clone

    def is_under_attack(self, colours="bw"):
        moves = []
        for col in list(colours):
            moves += [m for m in self._gamestate.get_pseudolegal_moves(
                col, get_castling_moves=False)]

        for move in moves:
            if type(move) == Move:
                if move.position_to == self.position:
                    return True
        else:
            return False

    @property
    def position(self):
        """
        The position of the square of the board denoted by a tuple : (x :int,y :int)
        """
        return self._position

    @position.setter
    def position(self, pos):
        game = self._gamestate
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
        if not p:
            self._gamestate.print()
            raise Exception("Can't pop_piece if there isn't one")
        p.position = (None, None)
        self._piece = None
        return p

    def get_piece(self):
        """
        Returns the current piece without setting the piece attribute to None
        Essentially returns a refrence to the piece
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
