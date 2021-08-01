from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove
from chess_game.GameState import GameState

g = GameState(fen_string="r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
king = g.get_square((4, 0)).get_piece()
king.get_legal_moves(g)
g.print()
