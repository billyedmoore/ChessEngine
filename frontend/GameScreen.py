import pygame
from chess_game import Game, Player


class Board(pygame.Surface):
    def __init__(self, parent_surface, x, y, total_side_length,
                 white_colour=(80, 80, 80), black_colour=(54, 54, 54)):
        self.x = x
        self.y = y
        self.black_colour = black_colour
        self.white_colour = white_colour
        self.white_player = ClientPlayer("w", self)
        self.black_player = ClientPlayer("b", self)
        self.game = Game.Game(self.white_player, self.black_player)
        self.create_sprites()
        self.parent_surface = parent_surface
        pygame.Surface.__init__((self), size=(
            total_side_length, total_side_length))

    def create_sprites(self):
        white_piece_things = self.game.get_one_colour_board("w")
        black_piece_things = self.game.get_one_colour_board("b")
        self.white_pieces = pygame.sprite.Group()
        self.black_pieces = pygame.sprite.Group()

    def draw_squares(self):
        square_width = self.get_width()//8
        colour_bit = True
        for x in range(8):
            colour_bit = not colour_bit
            for y in range(8):
                pygame.draw.rect(self, (self.white_colour if colour_bit else self.black_colour),
                                 (x*square_width, y*square_width, square_width, square_width))
                colour_bit = not colour_bit

    def draw(self):
        self.parent_surface.blit(self, (self.x, self.y))
        self.draw_squares()
        # self.fill(self.white_colour)

    def handle_event(self, event):
        pass


class ClientPlayer(Player.BasePlayer):
    def __init__(self, colour, board):
        self.board = board
        super().__init__(colour)

    def get_next_move(self):
        return board.get_next_move(self.colour)


class GameScreen(pygame.Surface):
    """
    Page to display and play a chess game with a specified set of options.
    """

    def __init__(self, app, w, h):
        pygame.Surface.__init__((self), size=(w, h))
        self.surface = app.screen  # surface refers to parent surface
        self.board = Board(self, h-h/4, h/20, w/2)

    def draw(self):
        self.fill((20, 20, 20))
        self.board.draw()
        self.surface.blit(self, (0, 0))

    def handle_event(self, event):
        pass
