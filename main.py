from chess_game.Pieces import Pawn
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState()
# print(g._squares[13]._piece.get_legal_moves(g))
m = Move((0, 1), (1, 1))
g.make_move(m)
g.print()
