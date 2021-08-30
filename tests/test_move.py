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

    def test_to_algebraic_notation_promotion(self):
        """
        Tests PromotionMove.to_algebraic_notation()
        """
        gs = GameState.GameState(
            fen_string="7k/PP1PP3/8/8/8/8/1P3PPP/RNBQKBNR w KQ - 0 1")
        mvs = [mv.to_algebraic_notation()
               for mv in gs.get_legal_moves("w") if mv.promotion]
        self.assertEqual(['Pa7a8=Q', 'Pb7b8=Q', 'Pd7d8=Q', 'Pe7e8=Q'], mvs)

    def test_to_algebraic_notation_castling_kingside(self):
        """
        Tests CastlingMove.to_algebraic_notation() for kingside moves
        """
        gs = GameState.GameState(
            fen_string="r3kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1")
        mv = Move.CastlingMove(gs, (4, 7), "k")
        self.assertEqual(mv.to_algebraic_notation(), "O-O")

    def test_to_algebraic_notation_castling_queenside(self):
        """
        Tests CastlingMove.to_algebraic_notation() for queenside moves
        """
        gs = GameState.GameState(
            fen_string="r3kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1")
        mv = Move.CastlingMove(gs, (4, 7), "k")
        gs.make_move(mv)
        mv = Move.CastlingMove(gs, (4, 0), "q")
        self.assertEqual(mv.to_algebraic_notation(), "O-O-O")

    def test_to_algebraic_notation_normal(self):
        """
        Tests Move.to_algebraic_notation() for normal_moves
        """
        def move_to_str(mv):
            if not mv.normal:
                return ""
            else:
                return f"{mv.position_from} -> {mv.position_to}"

        gs = GameState.GameState()
        mvs = [mv.to_algebraic_notation() for mv in gs.get_legal_moves("w")]
        mvs = [Move.Move.from_algebraic_notation(gs, "w", mv) for mv in mvs]
        formated_mvs = [move_to_str(mv) for mv in mvs]
        other_formated_mvs = [move_to_str(mv)
                              for mv in gs.get_legal_moves("w")]
        self.assertTrue(formated_mvs == other_formated_mvs)
