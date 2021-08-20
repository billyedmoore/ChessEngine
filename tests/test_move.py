import unittest
from chess_game import Move, GameState


class TestMoveMethods(unittest.TestCase):

    def test_from_algebraic_notation_pawn(self):
        """
        Tests Move.from_algebraic_notation() for a pawn move.
        """
        gs = GameState.GameState()
        mv = Move.Move.from_algebraic_notation(gs, "w", "a4")

        self.assertTrue(mv and mv.normal and mv.position_from ==
                        (0, 6) and mv.position_to == (0, 4))

    def test_from_algebraic_notation_normal_move(self):
        """
        Tests Move.from_algebraic_notation() for a normal move (a queen move).
        """
        gs = GameState.GameState(
            fen_string="rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")

        mv = Move.Move.from_algebraic_notation(gs, "w", "Qd7x+")
        self.assertTrue(mv and mv.normal and mv.position_from ==
                        (3, 7) and mv.position_to == (3, 1))

    def test_from_algebraic_notation_ambigous(self):
        """
        Tests Move.from_algebraic_notation() for a move where two pieces could 
        both move to that pos.
        """
        gs = GameState.GameState(
            fen_string="4k3/r2Q3r/8/8/8/8/3PPPPP/RNB1KBNR w KQ - 0 1")
        gs.make_move(Move.Move.from_algebraic_notation(gs, "w", "d4"))
        mv = Move.Move.from_algebraic_notation(gs, "b", "Rad7")
        self.assertTrue(mv and mv.normal and mv.position_from ==
                        (0, 1) and mv.position_to == (3, 1))
