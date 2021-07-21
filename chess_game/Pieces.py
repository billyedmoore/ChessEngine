from .Move import Move


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
    _move_count = 0
    _letter = "F"

    def __init__(self, position, color, move_count=0):
        self._move_count = move_count
        self._position = position
        self._colour = color

    @property
    def move_count(self) -> int:
        return self._move_count

    @property
    def letter(self) -> str:
        if self.colour.lower() == "w":
            return self._letter.upper()
        if self.colour.lower() == "b":
            return self._letter.lower()
        # TODO raise exception if color isn't in the set {"w","b"}

    @property
    def position(self) -> tuple:
        """
        The current position of the piece on the board in the form (x:int,y:int)
        """
        return self._position

    @position.setter
    def position(self, position) -> None:
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

    def make_move(self, position_to):
        self._moved = True
        self.position = position_to
        self._move_count += 1

    def get_legal_moves(self, game_state):
        pass

    def _get_possible_moves(self, game_state, directions, max_range=8):
        """
        Returns a list of moves without jumping pieces in given directions.
        To be used by Queen, King and Bishop.

        Parameters:
            GameState game_state - the current board position
            list<tuple<int,int>> directions - a list of directions denoted by
                                              tuples of int between -1 and 1
            int max_range - the distance from the current position the pieces
                            can go (allows for the King to move only 1)
        """
        diag_moves = []

        for direction in directions:
            for i in range(1, max_range):
                pos = (self.position[0]+(i*direction[0]),
                       self.position[1]+(i*direction[1]))
                if game_state.square_exists(pos):
                    diag_moves.append(Move(self.position, pos))
                    if not game_state.square_is_empty(pos):
                        break
        return diag_moves

    @colour.setter
    def colour(self, value):
        self._colour = value


class Pawn(Piece):
    """
    Implementation of Piece class
    """
    _letter = "P"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        legal_moves = []
        # print(self.colour.upper())

        colour_info = {
            "B": {"start_row": 1, "end_row": 7, "direction": +1},
            "W": {"start_row": 6, "end_row": 0, "direction": -1}}

        info = colour_info[self.colour.upper()]
        if self.position[1] == info["start_row"]:
            move_to = (self.position[0], self.position[1] +
                       (2*info["direction"]))
            if game_state.square_exists(move_to):
                legal_moves.append(Move(self.position, move_to))

        if self.position[1] != info["end_row"]:
            move_to = (self.position[0], self.position[1] +
                       (info["direction"]))
            if game_state.square_exists(move_to):
                legal_moves.append(Move(self.position, move_to))
        else:
            legal_moves.append(
                Move(self.position, self.position, promotion=True))

        # en-passant
        if self.position[1] == info["start_row"]+(2*info["direction"]):
            directions = [+1, -1]
            for direction in directions:
                if not game_state.square_is_empty((self.position[0]+direction, self.position[1])):
                    legal_moves.append(
                        Move(self.position, (self.position[0]+direction, self.position[1])))

        return legal_moves


class Bishop(Piece):
    """
    Implementation of Piece class
    """

    _letter = "B"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        directions = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
        legal_moves = self._get_possible_moves(game_state, directions)
        return legal_moves


class Queen(Piece):
    """
    Implementation of Piece class
    """

    _letter = "Q"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        directions = [(1, -1), (1, 0), (1, 1), (0, -1),
                      (0, 1), (-1, 1), (-1, -1), (-1, 0)]
        legal_moves = self._get_possible_moves(game_state, directions)
        return legal_moves


class King(Piece):
    """
    Implementation of Piece class
    """

    _letter = "K"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        directions = [(1, -1), (1, 0), (1, 1), (0, -1),
                      (0, 1), (-1, 1), (-1, -1), (-1, 0)]
        legal_moves = self._get_possible_moves(
            game_state, directions, max_range=2)
        return legal_moves


class Rook(Piece):
    """
    Implementation of Piece class
    """

    _letter = "R"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        directions = [(0, -1), (0, 1)]
        legal_moves = self._get_possible_moves(
            game_state, directions)
        return legal_moves


class Knight(Piece):
    """
    Implementation of Piece class
    """

    _letter = "N"

    # Don't like that you have to pass the game state numerous times
    def __init__(self, position, color, move_count=0):
        super().__init__(position, color, move_count=move_count)

    def get_legal_moves(self, game_state):
        legal_moves = []

        # Chose not to generate these programatically as would only slow down
        # the program and serve no real purpose other than showing off
        possible_changes = [(-2, -1), (-2, +1), (+2, -1),
                            (+2, +1), (-1, -2), (-1, +2), (+1, -2), (+1, +2)]

        for change in possible_changes:
            possible_move_to = (
                self.position[0]+change[0], self.position[1]+change[1])
            if game_state.square_exists(possible_move_to) and game_state.square_is_empty(possible_move_to):
                legal_moves.append(Move(self.position, possible_move_to))

        return legal_moves
