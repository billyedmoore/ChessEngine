from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove, CastlingMove
from chess_game.GameState import GameState

g = GameState(fen_string="4k3/8/8/8/8/8/8/R3K2R w - - 0 1")
print(g.get_square((4, 7)).get_piece().get_legal_moves(g))
g.print()
