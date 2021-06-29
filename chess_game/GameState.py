from .Square import Square


class GameState:
    """
    The current state of the game including the pieces & the Moves already made

    Methods:
        GameState(starting_position : string) (constructor)
        make_move(move: Move)
        square_exists(position: tuple(x,y))
        square_is_empty(position: tuple(x,y))
    """
    _squares = []

    # _squares = [Square(0,0),Square(0,1),...,Square(1,0),Square(1,1),...,Square(2,0)]

    def __init__(self,fen_string="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):

        ## To be replaced

        for x in range(8):
            for y in range(8):
                self._squares.append(Square((x,y)))

    def print(self):
        """
        prints the board to the terminal
        """

        output_string = ""
        current_row = 0
        for square in range(len(self._squares)):
            if square // 8 != current_row:
                output_string += "\n"
                current_row = square // 8
            empty = self._squares[square].is_empty()
            if empty:
                output_string += " "
            else:
                output_string += self._squares[square].get_piece().letter

        print(output_string)

    def make_move(self, move):
        pass

    def square_exists(self, position: tuple):
        """
        Checks if a square (denoted by some coords) exists
        """
        # Placeholder until I implement properly
        if position[0] >= 8:
            return False
        elif position[1] < 0:
            return False

    def square_is_empty(self, position: tuple):
        return True
