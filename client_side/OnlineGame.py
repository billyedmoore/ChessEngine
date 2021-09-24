
class OnlineGame():

    def __init__(self, app):
        self.game_id = app.client.join_game()
    @property
    def is_game_over(self):
        return self.app.client.is_game_over()

    @property
    def player_to_play(self):
        return self.app.client.get_player_to_play()

    def get_legal_moves(self):
        return self.app.client.get
    def get_one_colour_board(self, colour):
        return self.app.client.get_one_colour_board()

    def make_move(self, move):
        return self.app.client.make_move(move)

