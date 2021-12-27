# frontend/ConnectionErrorScreen.py
import pygame
from .SimpleTextScreen import SimpleTextScreen
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN
from time import sleep


class ConnectionErrorScreen(SimpleTextScreen):
    def __init__(self, app, w, h,
                 heading_text="Connection Error",
                 body_text=[
                     "Unfortunatly you've lost connection to the server.",
                     "Press any key to return to the log in screen."],
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
            self.app.open_login_screen()
