from .. import Player
from .Evaluation import Evaluation


class AIPlayer(Player.BasePlayer):
    def __init__(self, colour):
        super().__init__(colour)

    def get_next_move(self):
        best_value = (+10000000 if self.colour.lower() == "w" else -10000000)
        best_move = None
        print(self.gamestate.player_to_play)
        for move in self.gamestate.get_legal_moves(self.colour):
            gs_cpy = self.gamestate.clone()
            move_cpy = move.clone()
            move_cpy.gamestate = gs_cpy
            gs_cpy.make_move(move_cpy)

            value = self.alphabeta(gs_cpy, 2, -10000000,
                                   +10000000, (True if self.colour.lower() == "w" else False))
            if self.colour.lower() == "w":
                if best_value > value:
                    best_value = value
                    best_move = move
            elif self.colour.lower() == "b":
                if best_value < value:
                    best_value = value
                    best_move = move
        print(
            f"selected move {best_move} {best_move.position_from} {best_move.position_to}")
        return best_move

    @ staticmethod
    def alphabeta(gamestate, depth, alpha, beta, maximising):
        """
        Implementation of the alphabeta pruning algorithm

        Parameters:
            GameState gamestate - the position at the current time
            int depth - the depth of moves still to evaluate
            int alpha - the minimum score
            int beta - the maximum score
        """

        # inspiration - https://www.cs.cornell.edu/courses/cs312/2002sp/lectures/rec21.htm
        if depth == 0:
            return Evaluation.evaluate(gamestate)

        if maximising:
            value = alpha
            for move in gamestate.get_legal_moves(gamestate.player_to_play):
                gs = gamestate.clone()
                move.gamestate = gs
                if not move.is_legal_move():
                    continue
                gs.make_move(move)
                value = max(value, AIPlayer.alphabeta(
                    gs, depth-1, alpha, beta, False))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = beta
            for move in gamestate.get_legal_moves(gamestate.player_to_play):
                gs = gamestate.clone()
                move.gamestate = gs
                if not move.is_legal_move():
                    continue
                gs.make_move(move)
                value = min(value, AIPlayer.alphabeta(
                    gs, depth-1, alpha, beta, True))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value
