from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove, CastlingMove
from chess_game.GameState import GameState
from chess_game.Player import TerminalPlayer
from chess_game.Game import Game

# g = GameState(
# fen_string="1nbqkbn1/8/r6r/8/8/1PPP1BN1/PPNBQPPP/R3K2R w KQ - 0 1")
game = Game(TerminalPlayer("w"), TerminalPlayer("b"))
game.print()
while True:
    # if game._gamestate.checkmate("w"):
    # print("black wins")
    # elif game._gamestate.checkmate("b"):
    # print("white wins")
    game.play_next_move()
    game.print()
    print([f"{m.position_from} -> {m.position_to}" for m in game._gamestate.get_pseudolegal_moves(
        game._gamestate.player_to_play) if m.normal])
    print(game._gamestate.get_legal_moves(game._gamestate.player_to_play))
