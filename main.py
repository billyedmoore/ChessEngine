from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState(
    fen_string="7k/1R6/R7/8/8/8/8/3QKP2 w - - 0 1")

# g.print()
# print(g.check)
print(g.checkmate)
