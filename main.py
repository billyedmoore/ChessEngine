from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove, CastlingMove
from chess_game.GameState import GameState
from chess_game.Player import TerminalPlayer
from chess_game.Game import Game

# g = GameState(
# fen_string="1nbqkbn1/8/r6r/8/8/1PPP1BN1/PPNBQPPP/R3K2R w KQ - 0 1")

w_player = TerminalPlayer("w")
b_player = TerminalPlayer("b")

game = Game(w_player, b_player)
game_over = False
while not game_over:
    game.play_next_move()
    if game.gamestate.checkmate("w"):
        print("checkmate white wins")
        game_over = True
    elif game.gamestate.checkmate("b"):
        print("checkmate black wins")
        game_over = True

print(game.gamestate.check("w"))
print(game.gamestate.check("b"))
