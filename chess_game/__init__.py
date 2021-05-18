"""chess_game module

Implementation of chess rules.

Classes:
    GameState - The current position of the board & the moves already made & the pieces on the board
    Piece (Abstract) - The abstract class for a piece
        King
        Queen
        Rook
        Knight
        Bishop
        Pawn
    Move - Represents the movement from one square to another
"""

class GameState:
    """
    The current state of the game including the Pieces and moves already made

    Methods:
        GameState(starting_position : string);

    """
