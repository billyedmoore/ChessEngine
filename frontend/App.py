from . import LoginScreen, MenuScreen
import pygame
from pygame.locals import *
import sys
pygame.init()


class App:
    """
    Main loop of pygame frontend
    """

    def __init__(self):
        pygame.display.set_caption("ChessEngine")

        self.in_game = False
        self.screen_res = [960, 540]
        self.screen = pygame.display.set_mode(
            self.screen_res, pygame.HWSURFACE, 32)
        self.current_screen = LoginScreen.LoginScreen(
            self, self.screen_res[0], self.screen_res[1])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("freemono", 20)
        self.last_tick = pygame.time.get_ticks()

        while True:
            self.loop()

    def loop(self):
        self.event_loop()

        self.tick()
        self.draw()

    def event_loop(self):
        for event in pygame.event.get():
            self.current_screen.handle_event(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def tick(self):
        self.ttime = self.clock.tick()
        self.current_screen.tick()

    def open_menu(self):
        menuscreen = MenuScreen.MenuScreen(
            self, self.screen_res[0], self.screen_res[1])
        self.current_screen = menuscreen

    def start_game(self, game_screen):
        self.in_game = True
        self.current_screen = game_screen

    def draw(self):
        self.screen.fill((57, 62, 70))
        self.current_screen.draw()
        pygame.display.update()
