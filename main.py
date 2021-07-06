from chess_game.Pieces import Pawn
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState()
m = Move((1, 7), (1, 3))
g.make_move(m)
g.print()
