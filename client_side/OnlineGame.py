class OnlineGame:

    def __init__(self, app):
        self.game_id = app.client.join_game()

    @property
    def is_game_over(self):
        return self.app.client.is_game_over()

    @property
    def player_to_play(self):
        return self.app.client.get_player_to_play()

    def get_legal_moves(self):
        return self.app.client.get_legal_moves()

    def possible_move_positions_for_piece(self, coord):
        return self.app.client.possible_move_positions_for_piece()

    def get_previous_moves(self, colour):
        return self.app.client.get_previous_moves(colour)

    def get_one_colour_board(self, colour):
        return self.app.client.get_one_colour_board(colour)

    def tick(self):
        return self.app.client.tick()

    def make_move(self, move):
        return self.app.client.make_move(move)

    def get_algebraic_notation(self, pos_from, pos_to):
        return self.app.client.get_algebraic_notation(pos_from, pos_to)
