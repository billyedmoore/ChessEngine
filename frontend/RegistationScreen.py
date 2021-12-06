import pygame


class RegistrationScreen(pygame.Surface):

    def __init__(self, app, w, h):
        pygame.Surface.__init__(self, size=(w, h))
        self.surface = app.screen
        self.app = app
        self.elements = []

    def handle_event(self, event):
        [elem.handle_event(event) for elem in self.elements]

    def registation_attempt(self):
        pass

    def tick(self):
        pass

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((20, 20, 20))
        [elem.draw() for elem in self.elements]
