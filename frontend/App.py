from . import LoginScreen, MenuScreen, RegistationScreen
from client_side.Client import Client
import pygame
from pygame.locals import *
import sys
pygame.init()


class App:
    """
    Main loop of pygame frontend
    """
    user = None
    in_game = False
    screen_res = [960, 540]

    def __init__(self, host="127.0.0.1", port=65432):
        pygame.display.set_caption("ChessEngine")
        self.client = Client(self, host, port)
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

    def handle_login(self, user):
        self.user = user
        menuscreen = MenuScreen.MenuScreen(
            self, self.screen_res[0], self.screen_res[1])
        self.current_screen = menuscreen

    def open_registration_screen(self):
        self.current_screen = RegistationScreen.RegistrationScreen(
            self, self.screen_res[0], self.screen_res[1])

    def start_game(self, game_screen):
        self.in_game = True
        self.current_screen = game_screen

    def draw(self):
        self.screen.fill((57, 62, 70))
        self.current_screen.draw()
        pygame.display.update()
