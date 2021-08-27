import pygame
from pygame.locals import *


class Button(pygame.Surface):
    def __init__(self, surface, w, h, x, y, text="Hello World!",
                 inactive_colour=(80, 80, 80), hover_colour=(65, 65, 65),
                 font=None,
                 on_click=lambda: print("Button Pressed!")):
        self.hover = False
        self.text = text
        self.font = font if font else pygame.font.SysFont("freemono", 20)
        self.on_click = on_click
        self.hover_colour = hover_colour
        self.inactive_colour = inactive_colour
        self.surface = surface
        self.x = x
        self.y = y
        pygame.Surface.__init__(self, size=(w, h))
        self.fill(inactive_colour)

    def draw(self):
        colour = self.hover_colour if self.hover else self.inactive_colour
        self.fill(colour)
        text = self.font.render(self.text, 1, (255, 255, 255))
        self.blit(text, (10, 10))
        self.surface.blit(self, (self.x, self.y))

    def handle_event(self, event):
        """
        Handles MOUSEBUTTONDOWN events
        """
        accepted_event_types = [MOUSEBUTTONDOWN, MOUSEMOTION]
        if not event or event.type not in accepted_event_types:
            return
        if not self.hover and self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
            self.hover = True
        elif self.hover and not self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
            self.hover = False

        if event.type == MOUSEBUTTONDOWN and self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
            self.on_click()
