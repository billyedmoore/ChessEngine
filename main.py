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
m_three = Move((3, 0), (3, 2))
g.make_move(m_three)
g.print()
m_four = Move((4, 0), (3, 0))
g.make_move(m_four)
g.print()
