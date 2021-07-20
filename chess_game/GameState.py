from .Square import Square
from .Pieces import Rook, Pawn, Bishop, King, Knight, Queen


class MoveStack:
    """
    Dynamic length stack to store the moves made in a game
    Basically a glorified property
    """
    _moves = []

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
        value = self._moves[length - 1]
        del self._moves[length - 1]
        return value

    def peek(self):
        """
        Returns the top item from the stack without removing it from the stack
        """
        return self._moves[len(self._moves) - 1]


class GameState:
    """
    The current state of the game including the pieces & the Moves already made

    Methods:
        GameState(starting_position : string) (constructor)
        _load_fen(fen_string: string)
        make_move(move: Move)
        square_exists(position: tuple(x,y))
        square_is_empty(position: tuple(x,y))
    """
    _squares = []
    _captured_pieces = []
    _moves = MoveStack()

    # _squares = [Square(0,0),Square(0,1),...,Square(1,0),Square(1,1),...,Square(2,0)]

    def __init__(self, fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self._load_fen(fen_string)

    @property
    def ply_count(self):
        return self._moves.ply_count

    def _load_fen(self, fen_string):
        """
        load the pieces on the board from a FEN string (https://www.chessprogramming.org/Forsyth-Edwards_Notation).
        Should only be called by the constructor

        Parameters:
            fen_string: a string that follows FEN notation (https://www.chessprogramming.org/Forsyth-Edwards_Notation)
        """
        letter_lookup = {"r": Rook, "n": Knight,
                         "p": Pawn, "b": Bishop, "k": King, "q": Queen}

        ranks = fen_string.split(" ")[0].split("/")

        for rank_index in range(len(ranks)):
            squares = []
            skip_counter = 0  # the number of empty squares before the next full one
            chars_evaluated = 0  # the number of chars of the rank that have already been acted upon
            for x in range(8):  # for each row of the chessboard
                squares.append(Square((x, rank_index)))
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
                        letter_lookup[ranks[rank_index][chars_evaluated].lower()](squares[x].position, color))
                    chars_evaluated += 1

            self._squares.extend(squares)  # overwrites the current squares

    def print(self):
        """
        prints the board to the terminal **NOT** intended for use in final product
        """

        current_row = 0
        output_string = f"{' ' * 3} A B C D E F G H\n{' ' * 4}{'_ ' * 8}\n{current_row + 1} | "
        for square in range(len(self._squares)):
            if square // 8 != current_row:
                current_row = square // 8
                output_string += f"\n{current_row + 1} | "
            empty = self._squares[square].is_empty()
            if empty:
                output_string += "  "
            else:
                output_string += f"{self._squares[square].get_piece().letter} "
        print(output_string)

    def generate_fen(self):
        """
        Generate fen of the current position
        intended for use in debugging more than the actual game
        """
        pass

    def make_move(self, move):
        """
        Play a move on the GameState
        """
        square_from = self.get_square(move.position_from)

        piece = square_from.get_piece()  # only a copy as the move may be invalid
        square_to = self.get_square(move.position_to)
        formated_moves = [(m.position_from, m.position_to, m.promotion)
                          for m in piece.get_legal_moves(self)]
        print(formated_moves)
        if (square_from.position, square_to.position, move.promotion) not in formated_moves:
            raise Exception(
                f"Invalid Move {(square_from.position,square_to.position)}")

        # now the move is valid remove piece from square_from
        square_from.pop_piece()
        if move.promotion:
            square_from.set_piece(move.promote_to(
                square_from.position, piece.colour, move_count=piece.move_count))
        else:
            if not self.square_is_empty(square_to.position):
                captured_piece = square_to.pop_piece()
                self._captured_pieces.append(captured_piece)
            piece.make_move(square_to.position)
            square_to.set_piece(piece)
        self._moves.push(move)

    def get_square(self, position: tuple):
        return(self._squares[position[0] +
                             (position[1] * 8)])

    def square_exists(self, position: tuple):
        """
        Checks if a square (denoted by some coords) exists
        """
        def pos_in_range(pos):
            return(pos < 8 and pos >= 0)

        return(pos_in_range(position[0]) and pos_in_range(position[1]))

    def square_is_empty(self, position: tuple):
        square_index = position[1]*8 + position[0]
        return not bool(self._squares[square_index]._piece)
