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
    _promote_from = None

    # set to the piece captured in this move if one is to allow move to be undone
    _captured = None

    def __init__(self, gamestate, from_pos, to_pos, promotion=False, promote_to=None):
        self._gamestate = gamestate
        self._promotion = promotion
        self._promote_to = promote_to
        self._position_from = from_pos

        # so promotion can be undone
        self._promote_from = type(
            gamestate.get_square(self._position_from)._piece)
        self._position_to = to_pos

    def is_legal_move(self):
        square_from = self._gamestate.get_square(self.position_from)
        piece = square_from.get_piece()  # not pop incase move fails
        square_to = self._gamestate.get_square(self.position_to)
        formated_moves = [(m.position_from, m.position_to, m.promotion)
                          for m in piece.get_legal_moves(self._gamestate)]
        # print(formated_moves)
        if (square_from.position, square_to.position, self.promotion) not in formated_moves:
            return False
        else:
            return True

    def is_valid_position(self, position: tuple):
        for i in position:
            if type(i) != int:
                return False
            if i in range(0, 8):
                return True

    @property
    def captured(self):
        return self._captured

    @captured.setter
    def captured(self, piece):
        self._captured = piece

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
