from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState()
p = g.get_square((3, 1)).get_piece()
print(p._move_count)
# print(g._squares[13]._piece.get_legal_moves(g))
g.print()
m_three = Move((3, 1), (3, 3))
g.make_move(m_three)

last_pos = (3, 3)
for i in range(4, 8):
    m = Move(last_pos, (3, i))
    last_pos = (3, i)
    g.make_move(m)
    g.print()

m = Move((3, 7), (3, 7), promotion=True, promote_to=Queen)

print(p._move_count)
