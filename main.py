from chess_game.Player import TerminalPlayer
from chess_game.Game import Game
from chess_game.ai_player.AIPlayer import AIPlayer

w_player = TerminalPlayer("w")
b_player = AIPlayer("b")
game = Game(w_player, b_player)
while True:
    game.gamestate.print()
    game.play_next_move()
    mvs = game.gamestate.get_legal_moves(game.gamestate.player_to_play)
    print([mv.to_algebraic_notation() for mv in mvs])
    if game.is_game_over:
        break
