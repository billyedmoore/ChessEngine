from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move
from chess_game.GameState import GameState

g = GameState(
    fen_string="rnbqkbnr/pppp1ppp/3K4/4Qp2/8/8/PPPPPPPP/RNB2BNR w kq - 0 1")
g.print()
print(g.check)
