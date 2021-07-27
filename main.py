from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState(fen_string="1R5k/R7/8/8/8/8/8/1NBQKBN1 w - - 0 1")
g.print()
print(g.check("W"))
print(g.check("B"))
