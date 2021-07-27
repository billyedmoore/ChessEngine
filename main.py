from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState(fen_string="R6k/6R1/8/8/8/8/8/1NBQKBN1 w - - 0 1")
g.print()
print([(m.position_from, m.position_to) for m in g.get_legal_moves("B")])
print(g.checkmate("B"))
