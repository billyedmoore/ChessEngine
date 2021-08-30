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
        self.buttons = [Button(self, w/2, h/8, w/4, h/4,
                               text="Single Player",
                               on_click=lambda: app.start_game(GameScreen(app, w, h,black_player=AIPlayer("b")))),
                        Button(self, w/2, h/8, w/4, 2*(h/4),
                               text="Local Multiplayer",
                               on_click=lambda: app.start_game(GameScreen(app, w, h)))]

    def tick(self):
        pass

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((20, 20, 20))
        [button.draw() for button in self.buttons]

    def handle_event(self, event):
        [button.handle_event(event) for button in self.buttons]
