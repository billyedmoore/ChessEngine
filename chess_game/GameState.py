from .Square import Square
from .Pieces import Rook, Pawn, Bishop, King, Knight, Queen


class MoveStack:
    """
    Dynamic length stack to store the moves made in a game
    Basically a glorified property
    """
    _moves = []

    def __init__(self):
        self._moves = []

    def clone(self):
        cpy = MoveStack()
        cpy._moves = list(self._moves)
        return cpy

    def get_moves(self):
        return self._moves

    @property
    def ply_count(self):
        return len(self._moves)

    def push(self, move):
        """
        Adds a move to the top of the move stack
        """
        self._moves.append(move)

    def pop(self):
        """
        Returns and removes the top item from the stack
        """
        length = len(self._moves)
        if length == 0:
            return None
        value = self._moves[length - 1]
        del self._moves[length - 1]
        return value

    def peek(self):
        """
        Returns the top item from the stack without removing it from the stack
        """
        if len(self._moves) == 0:
            return None
        return self._moves[len(self._moves) - 1]


class GameState:
    """
    The current state of the game including the pieces & the Moves already made

    Methods:
        GameState(fen_string : string) (constructor) 
        _load_fen(fen_string: string)
        make_move(move: Move)
        square_exists(position: tuple(x,y))
        square_is_empty(position: tuple(x,y))
    """
    _squares = []
    _captured_pieces = []
    _moves = MoveStack()
    _player_to_play = "W"
    piece_letters = {"r": Rook, "n": Knight,
                     "p": Pawn, "b": Bishop, "k": King, "q": Queen}

    # _squares = [Square(0,0),Square(0,1),...,Square(1,0),Square(1,1),...,Square(2,0)]

    def __init__(self, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        """
        Parameters:
            string fen_string - string in fen format or empty string to not
                                generate a board of squares

        """
        if fen_string:
            self._load_fen(fen_string)

    def clone(self):
        """
        Creates a copy of the GameState
        """
        copy = GameState(fen_string="")
        copy._captured_pieces = [p.clone() for p in self._captured_pieces]
        squares = [s for s in self._squares]
        copy._squares = [s.clone(copy) for s in squares]
        copy._moves = self._moves.clone()
        return copy

    @property
    def ply_count(self):
        return self._moves.ply_count

    @property
    def player_to_play(self):
        return self._player_to_play

    @player_to_play.setter
    def player_to_play(self, player):
        if player.lower() in ["w", "b"]:
            self._player_to_play = player

    def check(self, colour: str) -> bool:
        """
        Returns a bool value repersenting wether the colour specified is in check

        Parameters
            string colour - value from the set {"w","W","b","B"}
        """
        opposition_colour = ["B", "W"][["W", "B"].index(colour.upper())]
        # TODO: handle no opposition_king on board
        try:
            opposition_king = [
                s._piece for s in self._squares
                if s._piece and s._piece.letter.lower() == "k"
                and s._piece.colour.upper() == colour.upper()][0]
            opposition_king_pos = opposition_king.position
        except IndexError:
            # self.print()
            return True

        # psuedolegal so it doesn't have to call game_state.check and get stuck
        # in infinite loop
        legal_moves = self.get_pseudolegal_moves(opposition_colour)

        for move in legal_moves:
            # if would capture king
            try:
                if move.position_to == opposition_king_pos:
                    return True
            except AttributeError:
                pass
        return False

    def checkmate(self, colour: str) -> bool:
        """
        Returns a bool value repersenting wether the colour specified is in 
        checkmate

        Parameters
            string colour - value from the set {"w","W","b","B"}
        """
        return(len(self.get_legal_moves(colour)) == 0)

    def get_legal_moves(self, colour: str):
        """
        Gets legal moves for a given colour

        Parameters
            string colour - value from the set {"w","W","b","B"}
        """
        pieces_of_colour = self.get_pieces_by_colour(colour)
        legal_moves = []
        for piece in pieces_of_colour:
            legal_moves.extend(piece.get_legal_moves(self))
        return legal_moves

    def get_pseudolegal_moves(self, colour: str):
        """
        Gets psuedolegal moves for a given colour. Includes moves that don't
        break check when in check. To be used to determine check.

        Parameters
            string colour - value from the set {"w","W","b","B"}
        """
        pieces_of_colour = self.get_pieces_by_colour(colour)
        legal_moves = []
        for piece in pieces_of_colour:
            try:
                legal_moves.extend(piece.get_pseudolegal_moves(self))
            except TypeError as te:
                raise te
        return legal_moves

    def _load_fen(self, fen_string):
        """
        load the pieces on the board from a FEN string (https://www.chessprogramming.org/Forsyth-Edwards_Notation).
        Should only be called by the constructor

        Parameters:
            fen_string: a string that follows FEN notation (https://www.chessprogramming.org/Forsyth-Edwards_Notation)
        """
        letter_lookup = self.piece_letters
        self._squares = []
        number = 1
        # R1k5/7R/2Q3K1/8/8/6rq/PPPPPPPP/1NB2BNr b - - 0 1
        ranks = fen_string.split(" ")[0].split("/")

        for rank_index in range(len(ranks)):
            squares = []
            skip_counter = 0  # the number of empty squares before the next full one
            chars_evaluated = 0  # the number of chars of the rank that have already been acted upon
            for x in range(8):  # for each row of the chessboard
                squares.append(Square(self, (x, rank_index)))
                if skip_counter != 0:
                    skip_counter = skip_counter - 1
                    continue
                elif (ranks[rank_index][chars_evaluated]).isnumeric():
                    skip_counter += int(ranks[rank_index][chars_evaluated]) - 1
                    chars_evaluated += 1
                    continue
                else:
                    # in accordance with FEN notation white pieces are capitalised
                    if ranks[rank_index][chars_evaluated].islower():
                        color = "b"
                    else:
                        color = "w"

                    squares[x].set_piece(
                        letter_lookup[ranks[rank_index][chars_evaluated].lower()](number, squares[x].position, color))
                    number += 1
                    chars_evaluated += 1

            # Adds the values from this rank to the _squares list
            self._squares.extend(squares)

    def print(self):
        """
        prints the board to the terminal **NOT** intended for use in final product
        """

        current_row = 0
        output_string = f"{' ' * 3} a b c d e f g h\n{' ' * 4}{'_ ' * 8}\n{8-current_row} | "
        for square in range(len(self._squares)):
            if square // 8 != current_row:
                current_row = square // 8
                output_string += f"\n{8-(current_row)} | "
            empty = self._squares[square].is_empty()
            if empty:
                output_string += "  "
            else:
                output_string += f"{self._squares[square].get_piece().letter} "
        print(output_string)

    def generate_fen(self):
        """
        Generate fen of the current position
        """
        fen_str = ""

        # for some reson this invents some kings
        pieces = [s.get_piece() for s in self._squares]
        board = [pieces[i:i+8] for i in range(0, 64, 8)]

        for row in board:
            counter = 0
            for y in row:
                if y:
                    if counter == 0:
                        fen_str += y.letter
                    else:
                        fen_str += f"{counter}{y.letter}"
                        counter = 0
                else:
                    counter += 1
            if counter != 0:
                fen_str += str(counter)
            fen_str += "/"

        return f"{fen_str[: -1]} {self._player_to_play.lower()}"

    def make_move(self, move, check_legality=True):
        """
        Play a move on the GameState
        """
        if move.gamestate != self:
            raise Exception(f"cant make move with diffrent gamestate")
        if check_legality and not move.is_legal_move():
            raise Exception(
                f"Invalid Move {(move.position_from,move.position_to)}")
        move.perform()

        self._moves.push(move)
        self._player_to_play = ["B", "W"][[
            "W", "B"].index(self._player_to_play)]

    def undo_move(self):
        move = self._moves.pop()
        move.unperform()

    def get_pieces_by_colour(self, colour: str):
        """
        Gets all of the pieces of a given colour.

        Parameters
            string colour - value from the set {"w","W","b","B"}
        """
        return [
            s._piece for s in self._squares if s._piece and
            s._piece.colour.upper() == colour.upper()]

    def get_square(self, position: tuple):
        """
        Gets a square at a given position

        Parameters:
            tuple position - a position in format (x,y) where (0 <= x,y <= 7)
        """
        return(self._squares[position[0] +
                             (position[1] * 8)])

    def get_move_stack(self):
        return self._moves

    @staticmethod
    def square_exists(position: tuple):
        """
        Checks if a square (denoted by some coords) exists

        Parameters:
            tuple position - a position in format (x,y) where (0 <= x,y <= 7)
        """
        def pos_in_range(pos):
            return(pos < 8 and pos >= 0)

        return(pos_in_range(position[0]) and pos_in_range(position[1]))

    def square_is_empty(self, position: tuple):
        """
        Checks if square at a given position is empty 

        Parameters:
            tuple position - a position in format (x,y) where (0 <= x,y <= 7)
        """
        square_index = position[1]*8 + position[0]
        return not bool(self._squares[square_index]._piece)
