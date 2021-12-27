import pygame
from client_side import OnlineGame
import threading
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from .Piece import Piece
from chess_game import Game, Move


class Board(pygame.Surface):
    down = False

    def __init__(self, app, parent_surface, x, y, total_side_length,
                 white_player=None, black_player=None,
                 white_colour=(90, 90, 90), black_colour=(40, 40, 40),
                 white_selected_colour=(200, 200, 200), black_selected_colour=(0, 0, 0),
                 online=False):

        self._from_pos = None
        self.app = app
        self.online = online
        self.x = x
        self.y = y
        self.square_width = total_side_length // 8
        self.black_colour = black_colour
        self.white_colour = white_colour
        self.white_player = white_player
        self.black_selected_colour = black_selected_colour
        self.white_selected_colour = white_selected_colour
        self.black_player = black_player

        # a list of moves possible for the piece currently selected
        self.possible_moves = []

        if not online:
            self.game = Game.Game(self.white_player, self.black_player)
        else:
            self.game = OnlineGame.OnlineGame(app)

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
                        Piece(white_piece_things[x][y][1], (x, y), self.square_width, white_piece_things[x][y][0], "w"))
                elif black_piece_things[x][y]:
                    self.black_pieces.add(
                        Piece(black_piece_things[x][y][1], (x, y), self.square_width, black_piece_things[x][y][0], "b"))

    @property
    def from_pos(self):
        return self._from_pos

    @from_pos.setter
    def from_pos(self, _from_pos):
        if _from_pos:
            self._from_pos = _from_pos
            self.possible_moves = self.game.possible_move_positions_for_piece(
                self._from_pos)
        else:
            self._from_pos = None
            self.possible_moves = []

    def update_sprites(self):
        """
        Update the position/existance of piece sprites based on the 
        "one_colour_board" from the Game/OnlineGame object
        """
        white_piece_things = self.game.get_one_colour_board("w")
        black_piece_things = self.game.get_one_colour_board("b")
        if not white_piece_things or not black_piece_things:
            return
        for x in range(8):
            for y in range(8):
                if white_piece_things[x][y]:
                    piece = [p for p in self.white_pieces.sprites() if p.number ==
                             white_piece_things[x][y][1]][0]
                    piece.pos = (x, y)
                    # piece.letter = white_piece_things[0]

                elif black_piece_things[x][y]:
                    piece = [p for p in self.black_pieces.sprites() if p.number ==
                             black_piece_things[x][y][1]][0]
                    piece.pos = (x, y)
                    # piece.letter = white_piece_things[0]

        white_pieces = [p for p in self.white_pieces.sprites() if p.number not in
                        [p[1] for p in sum(white_piece_things, []) if p]]
        black_pieces = [p for p in self.black_pieces.sprites() if p.number not in
                        [p[1] for p in sum(black_piece_things, []) if p]]

        self.white_pieces.remove(white_pieces)
        self.black_pieces.remove(black_pieces)

    def draw_squares(self):
        x_names = ["a", "b", "c", "d", "e", "f", "g", "h"]
        y_names = [str(num) for num in range(8, 0, -1)]
        square_width = self.get_width() // 8
        colour_bit = True
        for x in range(8):
            colour_bit = not colour_bit
            x_text = self.app.font.render(
                x_names[x], 1, (self.black_colour if colour_bit else self.white_colour))
            for y in range(8):
                y_text = self.app.font.render(
                    y_names[y], 1, (self.black_colour if colour_bit else self.white_colour))
                if (x, y) in self.possible_moves:
                    col = self.white_selected_colour if colour_bit else self.black_selected_colour
                else:
                    col = (self.white_colour if colour_bit else self.black_colour)
                pygame.draw.rect(self, col,
                                 (x * square_width, y * square_width, square_width, square_width))
                colour_bit = not colour_bit
                self.blit(y_text, (square_width*8 -
                                   (y_text.get_width()), y*square_width))
                # self.blit(y_text, (square_width*1 -
                                   # (y_text.get_width()), y*square_width))
            self.blit(x_text, (x * square_width, 0))

    def tick(self):
        # TODO: make this async so that it dont block the drawing
        game_over = self.game.is_game_over
        if not game_over:
            thread = threading.Thread(target=self.game.tick)
            thread.start()
            self.update_sprites()
        else:
            if game_over == "d":
                body = ["Thats a stalemate my friend.",
                        "Press any key to return to the menu."]
                self.app.open_game_over_screen(body=body)
            elif self.online:
                if game_over == self.game.colour_controlled:
                    body = ["You win, lets go.",
                            "Press any key to return to the menu."]
                    self.app.open_game_over_screen(body=body)
                else:
                    body = ["You lose, better luck next time.",
                            "Press any key to return to the menu."]
                    self.app.open_game_over_screen(body=body)
            elif game_over == "w":
                body = ["White wins, congats.",
                        "Press any key to return to the menu."]
                self.app.open_game_over_screen(body=body)
            elif game_over == "b":
                body = ["Black wins, congats.",
                        "Press any key to return to the menu."]
                self.app.open_game_over_screen()

        if not self.game.is_game_over:
            thread.join()

    def draw(self):
        self.parent_surface.blit(self,
                                 (self.x, self.y))
        self.draw_squares()
        self.white_pieces.update()
        self.black_pieces.update()
        if not self.game.is_game_over:
            self.white_pieces.draw(self)
            self.black_pieces.draw(self)
        # self.fill(self.white_colour)

    def handle_event(self, event):
        if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            if self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
                pos_in_board = (event.pos[0] - self.x, event.pos[1] - self.y)
                coord = (int((event.pos[0] - self.x) // self.square_width),
                         int((event.pos[1] - self.y) // self.square_width))
                if event.type == MOUSEBUTTONDOWN:
                    self.down = True
                    self.from_pos = coord
                    self.possible_moves = self.game.possible_move_positions_for_piece(
                        self.from_pos)
                elif event.type == MOUSEBUTTONUP:
                    if self.down and self.from_pos:
                        algebraic = self.game.get_algebraic_notation(
                            self.from_pos, coord)
                        print(algebraic)
                        self.game.make_move(algebraic)
                        # TODO handle castling moves and promotion moves
                    self.down = False
                    self.from_pos = None


class MoveTable(pygame.Surface):
    def __init__(self, app, parent_surface, x, y, w, h, game,
                 white_colour=(90, 90, 90), black_colour=(40, 40, 40)):
        pygame.Surface.__init__((self), size=(
            w, h))
        self.app = app
        self.game = game
        self.online = getattr(game,"online",False)
        self.black_colour = black_colour
        self.white_colour = white_colour
        self.big_font = pygame.font.SysFont(
                "freemono", 23)
        self.small_font = pygame.font.SysFont(
                "freemono", 25)
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.parent_surface = parent_surface

    def tick(self):
        pass

    def draw(self):
        prev_w_moves = self.game.get_previous_moves("w")
        prev_b_moves = self.game.get_previous_moves("b")
        if (not isinstance(prev_w_moves,list)
                or not isinstance(prev_b_moves,list)):
            return
        if len(prev_w_moves) > len(prev_b_moves):
            self.white_moves=prev_w_moves[-13:]
            self.black_moves=prev_b_moves[-12:]
        else:
            self.white_moves=prev_w_moves[-13:]
            self.black_moves=prev_b_moves[-13:]

        # Draw the "black" and "white" titles and the background for them
        if self.online:
            if self.game.colour_controlled.lower() == "w":
                white_text = "white(you)"
                black_text = "black"
            else:
                white_text = "white"
                black_text = "black(you)"
        else:
            white_text = "white"
            black_text = "black"

        white_title=self.big_font.render(white_text, 1, (255, 255, 255))
        black_title=self.big_font.render(black_text, 1, (255, 255, 255))
        header_height=white_title.get_height()*2.5
        w_rect=white_title.get_rect(
            center=(self.w/4, (header_height)/2))
        b_rect=black_title.get_rect(
            center=(self.w*3/4, (header_height)/2))
        pygame.draw.rect(self, self.white_colour,
                         (self.w / 2, 0,
                             self.w / 2, header_height))
        pygame.draw.rect(self, self.black_colour,
                         (0, 0,
                             self.w / 2, header_height))
        self.blit(white_title, w_rect)
        self.blit(black_title, b_rect)

        # Draw the backgrounds for the rest of the moves
        pygame.draw.rect(self, self.white_colour,
                         (0, header_height,
                          self.w / 2, self.h))
        pygame.draw.rect(self, self.black_colour,
                         (self.w / 2, header_height,
                          self.w / 2, self.h))
        # self.fill((90, 90, 90))
        text_height=30
        for move in range(len(self.white_moves)):
            text=self.small_font.render(
                self.white_moves[move], 1, (255, 255, 255))
            text_rect=text.get_rect(
                center=(self.w/4,
                        (text_height * move) +
                        header_height + 1/2*(text.get_height())))
            self.blit(text, text_rect)
        for move in range(len(self.black_moves)):
            text=self.small_font.render(
                self.black_moves[move], 1, (255, 255, 255))
            text_rect=text.get_rect(
                center=(self.w*3/4,
                        (text_height * move) +
                        header_height + 1/2*(text.get_height())))
            self.blit(text, text_rect)

        self.parent_surface.blit(self, (self.x, self.y))

    def handle_event(self, event):
        pass


class GameScreen(pygame.Surface):
    """
    Page to display and play a chess game with a specified set of options.
    """

    def __init__(self, app, w, h, white_player=None, black_player=None, online=False):
        pygame.Surface.__init__((self), size=(w, h))
        self.surface=app.screen  # surface refers to parent surface
        remaining_width=(h - h / 4)
        menu_screen_x=((w - remaining_width) - w / 2)
        self.board=Board(app, self, remaining_width, h / 20, w / 2,
                           white_player=white_player, black_player=black_player, online=online)
        self.move_table=MoveTable(
            app, self, menu_screen_x, h / 20, remaining_width - (1.5 * (menu_screen_x)), w / 2, self.board.game)
        self.fill((255, 255, 255))

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
