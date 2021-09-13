
class OnlineGame():

    def __init__(self, app):
        self.game_id = app.client.join_game()

    def get_one_colour_board(self, colour):
        return self.app.client.get_one_colour_board().get("board")

    def make_move(self, move):
        return self.app.client.make_move(move)
