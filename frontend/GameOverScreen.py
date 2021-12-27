import pygame
from .SimpleTextScreen import SimpleTextScreen
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN
from time import sleep


class GameOverScreen(SimpleTextScreen):
    """
    Screen shown to users at the end of a game. Displaying some text and
    allowing them to return to the home screen.
    """

    def __init__(self, app, w, h,
                 heading_text="Game Over",
                 body_text=[
                     "Well done you play a good game.",
                     "Press any key to return to the menu."],
                 big_font=None,
                 small_font=None
                 ):
        SimpleTextScreen.__init__(self, app, w, h,
                                  heading_text=heading_text,
                                  body_text=body_text,
                                  big_font=big_font,
                                  small_font=small_font)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            self.app.open_menu_screen()
