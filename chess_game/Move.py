class BaseMove:
    """
    A class to represent a move.
    Move is not aware of the game board ∴ doesn't validate anything.

    Properties:
        position_from - The current location of the piece
        position_to - Were the piece will be moved to
    """

    def __init__(self, gamestate):
        self._gamestate = gamestate

    def clone(self):
        pass

    def is_valid_position(self, position: tuple):
        for i in position:
            if type(i) != int:
                return False
            if i in range(0, 8):
                return True

    def perform(self):
        """
        Perform the move on the 'gamestate'
        """
        pass

    def unperform(self):
        if not self._gamestate.get_move_stack().peek() == self:
            raise Exception("Can only unperform the last move.")
        self._unperform()

    def _unperform(self):
        pass

    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, gamestate):
        self._gamestate = gamestate

    @ property
    def promotion(self):
        return (type(self) == PromotionMove)

    @ property
    def normal(self):
        return (type(self) == Move)

    @ property
    def castling(self):
        return (type(self) == CastlingMove)

    @staticmethod
    def from_algebraic_notation(gamestate, colour_moving, algebraic_move):
        """
        returns a Move formulated from an algebraic notation
        """
        # This is the worst function I have ever written
        piece_letters = ["R", "N", "P", "B", "K", "Q"]
        file_values = ["a", "b", "c", "d", "e", "f", "g", "h"]
        rank_values = ["8", "7", "6", "5", "4", "3", "2", "1"]

        def get_king(colour):
            king = [p for p in gamestate.get_pieces_by_colour(colour)
                    if p.letter.upper() == "K"][0]
            return king

        def coord_to_pos(coord):
            try:
                return (file_values.index(coord[0]), rank_values.index(coord[1]))
            except ValueError:
                return None

        if not algebraic_move:
            return None

        # ignore captures and checks as not relevant or helpful
        algebraic_move = "".join(
            [char for char in algebraic_move if char != "+" and char != "x"])

        # if no piece is stated then a pawn is moving
        if algebraic_move[0] in file_values:
            algebraic_move = "P" + algebraic_move

        # denotes a promotion move
        if "=" in algebraic_move:
            pass
        elif algebraic_move[0] in piece_letters:
            coord = coord_to_pos(algebraic_move[-2:])
            if not coord:
                return None
            possible_moves = [
                m for m in gamestate.get_legal_moves(colour_moving)
                if type(m) == Move and
                m.position_to == coord
                and gamestate.get_square(m.position_from).get_piece().letter.upper() == algebraic_move[0]]
            if len(possible_moves) == 1:
                return possible_moves[0]
            elif len(possible_moves) == 0:
                return None
            else:
                print(
                    [f"{m.position_from} -> {m.position_to}" for m in possible_moves])
                splice = algebraic_move[1:-2]
                if len(splice) == 2:
                    possible_moves == [
                        m for m in possible_moves if m.position_from == coord_to_pos(splice)]
                elif len(splice) == 1:
                    possible_moves_cpy = possible_moves
                    possible_moves = []
                    if splice in file_values:
                        for m in possible_moves_cpy:
                            if m.position_from[0] == file_values.index(splice):
                                possible_moves.append(m)

                        if len(possible_moves) != 1:
                            return None
                        else:
                            return possible_moves[0]
                    if splice in rank_values:
                        for m in possible_moves_cpy:
                            if m.position_from[1] == rank_values.index(splice):
                                possible_moves.append(m)
                        if len(possible_moves) != 1:
                            return None
                        else:
                            return possible_moves[0]
                else:
                    return None

                print(
                    f"move = {algebraic_move}| splice = {algebraic_move[1:-2]}")

        elif algebraic_move.strip() == "O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "k")
        elif algebraic_move.strip() == "O-O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "q")
        else:
            pass


class Move(BaseMove):
    # set to the piece captured in this move if one is to allow move to be undone
    _captured_piece = None

    def __init__(self, gamestate, from_pos, to_pos):
        super().__init__(gamestate)
        self._position_from = from_pos
        self._position_to = to_pos

    def clone(self):
        return Move(self.gamestate, self.position_from, self.position_to)

    @ property
    def captured(self):
        return self._captured_piece

    @ captured.setter
    def captured(self, piece):
        self._captured_piece = piece

    def is_legal_move(self):
        square_from = self._gamestate.get_square(self.position_from)
        piece = square_from.get_piece()
        square_to = self._gamestate.get_square(self.position_to)
        formated_moves = [(m.position_from, m.position_to)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.normal]]
        return ((square_from.position, square_to.position) in formated_moves)

    def perform(self):
        square_from = self._gamestate.get_square(self.position_from)
        square_to = self._gamestate.get_square(self.position_to)
        piece = square_from.pop_piece()
        if not self._gamestate.square_is_empty(square_to.position):
            captured_piece = square_to.pop_piece()
            self._captured_piece = (captured_piece)
        piece.make_move(square_to.position)
        square_to.set_piece(piece)

    def _unperform(self):
        square_from = self.get_square(self.position_from)
        square_to = self.get_square(self.position_to)
        piece = square_to.pop_piece()

        if self.captured:
            square_to.set_piece(self.captured)
        square_from.set_piece(piece)

    @ property
    def position_from(self):
        return self._position_from

    @ position_from.setter
    def position_from(self, pos):
        if self.is_valid_position(pos):
            self._position_from = pos

    @ property
    def position_to(self):
        return self._position_to

    @ position_to.setter
    def position_to(self, pos):
        if self.is_valid_position(pos):
            self._position_to = pos


class CastlingMove(BaseMove):
    _king_pos = (-1, -1)
    _side = ""

    def __init__(self, gamestate, king_pos, side):
        super().__init__(gamestate)
        self.king_position = king_pos
        self.side = side
        directions = {"q": -1, "k": 1}
        rook_positions = {
            "q": (0, self._king_pos[1]), "k": (7, self._king_pos[1])}
        self._king_to_pos = ((self.king_position[0] +
                              2*directions[self.side.lower()]), self.king_position[1])
        self._rook_to_pos = ((self.king_position[0] +
                              directions[self.side.lower()]), self.king_position[1])
        self._rook_from_pos = rook_positions[self.side.lower()]

    def clone(self):
        return CastlingMove(self.gamestate, self.king_position, self.side)

    def is_legal_move(self):
        # print(self.king_position)
        square = self._gamestate.get_square(self.king_position)
        piece = square.get_piece()
        formated_moves = [(m.king_position, m.side)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.castling]]
        return ((square.position, self.side) in formated_moves)

    def perform(self):
        king_from_square = self._gamestate.get_square(self._king_pos)
        rook_from_square = self._gamestate.get_square(self._rook_from_pos)
        king = king_from_square.get_piece()
        rook = rook_from_square.get_piece()

        king_to_square = self._gamestate.get_square(self._king_to_pos)
        king_to_square.set_piece(king)
        rook_to_square = self._gamestate.get_square(self._rook_to_pos)
        rook_to_square.set_piece(rook)

        king_from_square.pop_piece()
        rook_from_square.pop_piece()

    def _unperform(self):
        king_to_square = self._gamestate.get_square(self._king_to_pos)
        rook_to_square = self._gamestate.get_square(self._rook_to_pos)
        king = king_to_square.get_piece()
        rook = rook_to_square.get_piece()

        king_from_square = self._gamestate.get_square(self.king_pos)
        king_from_square.set_piece(king)
        rook_from_square = self._gamestate.get_square(self.rook_from_pos)
        rook_from_square.set_piece(rook)

        king_to_square.pop_piece()
        rook_to_square.pop_piece()

    @property
    def position_from(self):
        """
        legacy
        """
        return self._king_pos

    @ property
    def king_position(self):
        return self._king_pos

    @ king_position.setter
    def king_position(self, king_pos):
        if self.is_valid_position(king_pos):
            self._king_pos = king_pos

    @ property
    def side(self):
        return self._side

    @ side.setter
    def side(self, side):
        if side.lower() in ["k", "q"]:
            self._side = side


class PromotionMove(BaseMove):
    _promote_to = None
    _promote_from = None
    _position = (-1, -1)

    def __init__(self, gamestate, position, promote_to=None):
        super().__init__(gamestate)
        self._position = position
        self._promote_from = type(
            gamestate.get_square(self._position_from)._piece)
        self._promote_to = promote_to

    def clone(self):
        return PromotionMove(self.gamestate, self.position, self.promote_to)

    def is_legal_moves(self):
        square = self._gamestate.get_square(self.position)
        piece = square.get_piece()
        formated_moves = [(m.position)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.promotion]]
        return ((square.position) in formated_moves)

    def perform(self):
        square = self._gamestate.get_square(self.position)
        piece = square.pop_piece()
        piece_to_type = self.promote_to
        square.set_piece(piece_to_type(
            square.position, piece.colour, move_count=piece.move_count))

    def _unperform(self):
        square = self._gamestate.get_square(self.position)
        piece = square.pop_piece()
        piece_from_type = self.promote_from
        square.set_piece(piece_from_type(
            square.position, piece.colour, move_count=piece.move_count))

    @ property
    def promote_to(self):
        return self._promote_to

    @property
    def position_from(self):
        """
        legacy
        """
        return self.position

    @ property
    def position(self):
        return self.position

    @ position.setter
    def position(self, pos):
        if self.is_valid_position(pos):
            self._position = pos
