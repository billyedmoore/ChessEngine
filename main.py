from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState(
    fen_string="R1k5/7R/2Q3K1/8/8/6rq/PPPPPPPP/1NB2BNr b - - 0 1")
g.print()
print(g.check)
print(g.checkmate)
