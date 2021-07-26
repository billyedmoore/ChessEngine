from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState()

p = g.get_square((1, 1))._piece
new_piece = p.clone()
copy_of_board = g.clone()

m = Move(g, (1, 1), (1, 3))
g.make_move(m)
print("Original")
g.print()
print("Copy")
copy_of_board.print()

print(new_piece.position)
