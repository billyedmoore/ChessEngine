from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove
from chess_game.GameState import GameState

g = GameState(fen_string="1P6/7k/8/8/8/8/8/4K3 w - - 0 1")
pm = PromotionMove(g, (1, 0), promote_to=Queen)
g.make_move(pm)
g.print()
