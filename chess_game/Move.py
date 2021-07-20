class Move:
    """
    A class to represent a move.
    Move is not aware of the game board ∴ doesn't validate anything.

    Properties:
        position_from - The current location of the piece
        position_to - Were the piece will be moved to
    """

    _position_from = (-1, -1)
    _position_to = (-1, -1)
    _promotion = False
    _promote_to = None

    def __init__(self, from_pos, to_pos, promotion=False, promote_to=None):
        self._promotion = promotion
        self._promote_to = promote_to
        self._position_from = from_pos
        self._position_to = to_pos

    def is_valid_position(self, position: tuple):
        for i in position:
            if type(i) != int:
                return False
            if i in range(0, 8):
                return True

    @property
    def promotion(self):
        return self._promotion

    @property
    def promote_to(self):
        return self._promote_to

    @property
    def position_from(self):
        return self._position_from

    @position_from.setter
    def position_from_setter(self, pos):
        if self.is_valid_position(pos):
            self._position_from = pos

    @property
    def position_to(self):
        return self._position_to

    @position_to.setter
    def position_to_setter(self, pos):
        if self.is_valid_position(pos):
            self._position_to = pos
