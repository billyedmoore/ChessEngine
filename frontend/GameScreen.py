import pygame
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from .Piece import Piece
from chess_game import Game, Move


class Board(pygame.Surface):
    down = False

    def __init__(self, app, parent_surface, x, y, total_side_length,
                 white_player=None, black_player=None,
                 white_colour=(90, 90, 90), black_colour=(40, 40, 40)):
        self.app = app
        self.x = x
        self.y = y
        self.square_width = total_side_length//8
        self.black_colour = black_colour
        self.white_colour = white_colour
        self.white_player = white_player
        self.black_player = black_player
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

        for x in range(8):
            for y in range(8):
                if white_piece_things[x][y]:
                    self.white_pieces.add(
                        Piece(white_piece_things[x][y][1], (x, y), (320//8), white_piece_things[x][y][0], "w"))
                elif black_piece_things[x][y]:
                    self.black_pieces.add(
                        Piece(black_piece_things[x][y][1], (x, y), (320//8), black_piece_things[x][y][0], "b"))

    def update_sprites(self):
        white_piece_things = self.game.get_one_colour_board("w")
        black_piece_things = self.game.get_one_colour_board("b")
        for x in range(8):
            for y in range(8):
                if white_piece_things[x][y]:
                    piece = [p for p in self.white_pieces.sprites() if p.number ==
                             white_piece_things[x][y][1]][0]
                    piece._pos = (x, y)
                elif black_piece_things[x][y]:
                    piece = [p for p in self.black_pieces.sprites() if p.number ==
                             black_piece_things[x][y][1]][0]
                    piece._pos = (x, y)

        white_pieces = [p for p in self.white_pieces.sprites() if p.number not in
                        [p[1] for p in sum(white_piece_things, []) if p]]
        black_pieces = [p for p in self.black_pieces.sprites() if p.number not in
                        [p[1] for p in sum(black_piece_things, []) if p]]

        self.white_pieces.remove(white_pieces)
        self.black_pieces.remove(black_pieces)

    def draw_squares(self):
        x_names = ["a", "b", "c", "d", "e", "f", "g", "h"]
        square_width = self.get_width()//8
        colour_bit = True
        for x in range(8):
            colour_bit = not colour_bit
            text = self.app.font.render(
                x_names[x], 1, (self.black_colour if colour_bit else self.white_colour))
            for y in range(8):
                pygame.draw.rect(self, (self.white_colour if colour_bit else self.black_colour),
                                 (x*square_width, y*square_width, square_width, square_width))
                colour_bit = not colour_bit
            self.blit(text, (x*square_width, 0))

    def tick(self):
        # TODO: make this async so that it dont block the drawing
        if not self.game.is_game_over:
            self.game.tick()
        self.update_sprites()
        self.draw()

    def draw(self):
        self.parent_surface.blit(self, (self.x, self.y))
        self.draw_squares()
        self.white_pieces.update()
        self.black_pieces.update()
        self.white_pieces.draw(self)
        self.black_pieces.draw(self)
        # self.fill(self.white_colour)

    def handle_event(self, event):
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            if self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
                pos_in_board = (event.pos[0]-self.x, event.pos[1]-self.y)
                coord = (int((event.pos[0]-self.x)//self.square_width),
                         int((event.pos[1]-self.y)//self.square_width))
                if event.type == MOUSEBUTTONDOWN:
                    self.down = True
                    self.from_pos = coord
                elif event.type == MOUSEBUTTONUP:
                    if self.down and self.from_pos:
                        print(f"{self.from_pos} -> {coord}")
                        mv = Move.Move(self.game.gamestate,
                                       self.from_pos, coord)
                        self.game.make_move(mv.to_algebraic_notation())
                    self.down = False
                    self.from_pos = None


class MoveTable(pygame.Surface):
    def __init__(self, app, parent_surface, x, y, w, h, game):
        pygame.Surface.__init__((self), size=(
            w, h))
        self.app = app
        self.game = game
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.parent_surface = parent_surface

    def tick(self):
        pass

    def draw(self):
        self.white_moves = self.game.get_previous_moves("w")[-10:]
        self.black_moves = self.game.get_previous_moves("b")[-10:]
        self.parent_surface.blit(self, (self.x, self.y))
        self.fill((90, 90, 90))
        text_height = 30
        for move in range(len(self.white_moves)):
            text = self.app.font.render(
                self.white_moves[move], 0.5, (255, 255, 255))
            self.blit(text, (0, text_height*move))
        for move in range(len(self.black_moves)):
            text = self.app.font.render(
                self.black_moves[move], 1, (255, 255, 255))
            self.blit(text, (self.w/2, text_height*move))

    def handle_event(self, event):
        pass


class GameScreen(pygame.Surface):
    """
    Page to display and play a chess game with a specified set of options.
    """

    def __init__(self, app, w, h):
        pygame.Surface.__init__((self), size=(w, h))
        self.surface = app.screen  # surface refers to parent surface
        remaining_width = h-h/4
        self.board = Board(app, self, remaining_width, h/20, w/2)
        self.move_table = MoveTable(
            app, self, remaining_width/20, h/20, (remaining_width/20)*18, w/2,  self.board.game)
        self.fill((20, 20, 20))

    def draw(self):
        self.board.draw()
        self.move_table.draw()
        self.surface.blit(self, (0, 0))

    def tick(self):
        self.board.tick()
        self.move_table.tick()

    def handle_event(self, event):
        self.board.handle_event(event)
        self.move_table.handle_event(event)
