import pygame
from Button import Button
from pygame.locals import *


class MenuScreen(pygame.Surface):

    def __init__(self, app, w, h):
        pygame.Surface.__init__((self), size=(w, h))
        self.surface = app.screen
        button_width = w/2
        self.buttons = [Button(self, w/2, h/8, w/4, h/4,
                               text="Single Player"),
                        Button(self, w/2, h/8, w/4, 2*(h/4),
                               text="Local Multiplayer")]

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((34, 40, 49))
        [button.draw() for button in self.buttons]

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            [button.handle_event(event) for button in self.buttons]
