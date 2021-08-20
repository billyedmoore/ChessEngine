import unittest

from chess_game import GameState, Move


class TestGameStateMethods(unittest.TestCase):
    def test_ply_count(self):
        """
        Tests that the correct number of half moves have been counted
        """
        games = GameState.GameState()
        # not sure why I need this as no moves should have been made at this
        # point
        games.get_move_stack()._moves = []

        move = Move.BaseMove.from_algebraic_notation(games, "w", "a4")
        games.make_move(move)
        move = Move.BaseMove.from_algebraic_notation(games, "b", "a5")
        games.make_move(move)
        move = Move.BaseMove.from_algebraic_notation(games, "w", "b4")
        games.make_move(move)
        move = Move.BaseMove.from_algebraic_notation(games, "b", "b5")
        games.make_move(move)

        self.assertEqual(4, games.ply_count)

    def test_check(self):
        """
        Tests that check is correctly calculated
        """
        gs = GameState.GameState(
            fen_string="rnbqkbn1/pppppppp/8/8/4r3/8/PPPP1PPP/RNBQKBNR w KQq - 0 1")
        check_w = gs.check("w")
        gs = GameState.GameState(
            fen_string="rnbqkbnr/pppp1ppp/8/4Q3/8/8/PPPPPPPP/RNB1KBNR w KQkq - 0 1")
        check_b = gs.check("b")
        self.assertTrue(check_w and check_b)

    def test_checkmate(self):
        """
        Tests that checkmate is correctly calculated
        """
        gs = GameState.GameState(
            fen_string="1nbqkbn1/pppppppp/8/8/8/8/r7/4K2r w - - 0 1")
        checkmate = gs.checkmate("w")
        self.assertTrue(checkmate)


if __name__ == "__main__":
    unittest.main()
