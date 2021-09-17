import pygame
from pygame.locals import *


class TextBox(pygame.Surface):

    def __init__(self, surface, w, h, x, y, placeholder_text="", font=None,text="",
                 active_colour=(230, 230, 230), inactive_colour=(40, 40, 40),
                 text_hidden=False):
        pygame.Surface.__init__(self, size=(w, h))
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.placeholder_text = placeholder_text
        self.surface = surface
        self.font = font if font else pygame.font.SysFont("freemono", 20)
        self.text = text
        self.text_hidden = text_hidden
        self.text_surface = self.font.render(
            (self.text if not self.text_hidden else ("*"*len(self.text))), 1, (0, 0, 0))
        self.active_colour = active_colour
        self.inactive_colour = inactive_colour

        self.active = False

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.get_rect(topleft=(self.x, self.y)).collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif self.active and event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == K_RETURN:
                self.active = False
            else:
                self.text += event.unicode
            self.text_surface = self.font.render(
                (self.text if not self.text_hidden else ("*"*len(self.text))), 1, (0, 0, 0))

    def draw(self):
        colour = self.active_colour if self.active else self.inactive_colour
        self.surface.blit(self, (self.x, self.y))
        self.fill(colour)
        if not self.text:
            text_surface = self.font.render(
                self.placeholder_text, 1, (20, 20, 20))
        else:
            text_surface = self.text_surface

        text_rect = text_surface.get_rect(center=(self.w/2, self.h/2))
        self.blit(text_surface, text_rect)
