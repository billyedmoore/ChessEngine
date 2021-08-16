from chess_game.Pieces import Pawn, Queen
from chess_game.Move import Move, PromotionMove, CastlingMove
from chess_game.GameState import GameState
from chess_game.Player import TerminalPlayer
from chess_game.Game import Game
from chess_game.Move import Move
from chess_game.ai_player.AIPlayer import AIPlayer
from chess_game.ai_player.Evaluation import Evaluation

w_player = TerminalPlayer("w")
b_player = AIPlayer("b")
game = Game(w_player, b_player)
while True:
    game.gamestate.print()
    game.play_next_move()
