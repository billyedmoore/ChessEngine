from chess_game.Pieces import Pawn
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState()
# print(g._squares[13]._piece.get_legal_moves(g))
g.print()
m = Move((3, 1), (3, 3))
g.make_move(m)
g.print()
m_two = Move((2, 0), (4, 2))
g.make_move(m_two)

g.print()
