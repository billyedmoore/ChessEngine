

class BaseMove:
    """
    A class to represent a move.
    Move is not aware of the game board ∴ doesn't validate anything.

    Properties:
        position_from - The current location of the piece
        position_to - Were the piece will be moved to
    """

    # set to the piece captured in this move if one is to allow move to be undone
    _captured_pieces = []

    def __init__(self, gamestate):
        self._gamestate = gamestate

    def clone(self):
        return Move(self._gamestate, self.position_from, self.position_to, promotion=self.promotion, promote_to=self.promote_to)

    def is_valid_position(self, position: tuple):
        for i in position:
            if type(i) != int:
                return False
            if i in range(0, 8):
                return True

    def perform(self):
        pass

    @ property
    def captured(self):
        return self._captured

    @ captured.setter
    def captured(self, piece):
        self._captured = piece

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
        print("from_algebraic_notation")
        # print(algebraic_move)
        piece_letters = ["R", "N", "P", "B", "K", "Q"]
        file_values = ["a", "b", "c", "d", "e", "f", "g", "h"]
        rank_values = ["8", "7", "6", "5", "4", "3", "2", "1"]

        # TODO remove only for troubleshooting
        if not gamestate:
            print(f"{gamestate} - {colour_moving} - {algebraic_move}")

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
        print(algebraic_move)

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
                if algebraic_move[-3] in rank_values:
                    rank_values.index[algebraic_move[-3]]
                elif algebraic_move[-3] in file_values:
                    pass
                print(
                    "More than one move is possible and I cba to deal with that bs right now")
                print(possible_moves)
        elif algebraic_move.strip() == "O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "k")
        elif algebraic_move.strip() == "O-O-O":
            king = get_king(colour_moving)
            return CastlingMove(gamestate, king.position, "q")
        else:
            pass


class Move(BaseMove):
    def __init__(self, gamestate, from_pos, to_pos):
        super().__init__(gamestate)
        self._position_from = from_pos
        self._position_to = to_pos

    def is_legal_move(self):
        square_from = self._gamestate.get_square(self.position_from)
        piece = square_from.get_piece()
        square_to = self._gamestate.get_square(self.position_to)
        formated_moves = [(m.position_from, m.position_to)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.normal]]
        return ((square_from.position, square_to.position) in formated_moves)

    def perform(self):
        square_from = self._gamestate.get_square(self.position_from)
        piece = square_from.pop_piece()
        square_to = self._gamestate.get_square(self.position_to)
        if not self._gamestate.square_is_empty(square_to.position):
            captured_piece = square_to.pop_piece()
            self._captured_pieces.append(captured_piece)
        piece.make_move(square_to.position)
        square_to.set_piece(piece)

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

    def is_legal_move(self):
        # print(self.king_position)
        square = self._gamestate.get_square(self.king_position)
        piece = square.get_piece()
        formated_moves = [(m.king_position, m.side)
                          for m in [p for p in piece.get_legal_moves(self._gamestate) if p.castling]]
        return ((square.position, self.side) in formated_moves)

    def perform(self):
        rook_positions = {
            "q": (0, self._king_pos[1]), "k": (7, self._king_pos[1])}
        directions = {"q": -1, "k": 1}
        king_from_square = self._gamestate.get_square(self._king_pos)
        king = king_from_square.get_piece()
        rook_from_square = self._gamestate.get_square(
            rook_positions[self.side.lower()])
        rook = rook_from_square.get_piece()

        king_to_pos = ((self.king_position[0] +
                        2*directions[self.side.lower()]), self.king_position[1])
        rook_to_pos = ((self.king_position[0] +
                        directions[self.side.lower()]), self.king_position[1])

        king_to_square = self._gamestate.get_square(king_to_pos)
        king_to_square.set_piece(king)
        rook_to_square = self._gamestate.get_square(rook_to_pos)
        rook_to_square.set_piece(rook)

        king_from_square.pop_piece()
        rook_from_square.pop_piece()

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

    @ property
    def promote_to(self):
        return self._promote_to

    @ property
    def position(self):
        return self.position

    @ position.setter
    def position(self, pos):
        if self.is_valid_position(pos):
            self._position = pos
