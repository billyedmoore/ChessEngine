import pygame
from .Button import Button
from .GameScreen import GameScreen
from chess_game.ai_player.AIPlayer import AIPlayer
from pygame.locals import *


class MenuScreen(pygame.Surface):

    def __init__(self, app, w, h):
        pygame.Surface.__init__((self), size=(w, h))
        self.surface = app.screen
        button_width = w/2
        button_pos = self.get_button_pos(3, w, h)
        self.buttons = [Button(self, button_pos[0][0], button_pos[0][1], button_pos[0][2], button_pos[0][3],
                               text="Single Player",
                               on_click=lambda: app.start_game(GameScreen(app, w, h, black_player=AIPlayer("b")))),
                        Button(self, button_pos[1][0], button_pos[1][1], button_pos[1][2], button_pos[1][3],
                               text="Local Multiplayer",
                               on_click=lambda: app.start_game(GameScreen(app, w, h))),

                        Button(self, button_pos[2][0], button_pos[2][1], button_pos[2][2], button_pos[2][3],
                               text="Online Multiplayer",
                               on_click=lambda: app.start_game(GameScreen(app, w, h, online=True)))]

    @staticmethod
    def get_button_pos(num_buttons, w, h):
        """
        Gets the positions 
        """
        top_margin = h/4
        left_margin = w/4
        height_for_buttons = h - top_margin*2
        button_width = int(w/2)
        button_height = h/(num_buttons*3)
        gap = (height_for_buttons - (num_buttons*button_height))/(num_buttons-1)
        buttons = []
        for button in range(1, 1+num_buttons):
            w = button_width
            h = button_height
            x = left_margin
            y = top_margin+(button_height*(button-1)+(gap*(button-1)))
            buttons.append((w, h, x, y))
        return buttons

    def tick(self):
        pass

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((20, 20, 20))
        [button.draw() for button in self.buttons]

    def handle_event(self, event):
        [button.handle_event(event) for button in self.buttons]
