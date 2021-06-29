from chess_game.Pieces import Pawn
from chess_game import GameState

g = GameState()
p = Pawn(g, (0, 0))
p.game = 10
print(g.var)

