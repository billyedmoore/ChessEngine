import pygame
from . import TextBox, Button


class LoginScreen(pygame.Surface):

    def __init__(self, app, w, h):
        pygame.Surface.__init__(self, size=(w, h))
        self.surface = app.screen
        self.app = app
        self.elements = [
            TextBox.TextBox(self, w/2, h/8, w/4, (h/64)*17,
                            placeholder_text="username"),
            TextBox.TextBox(self, w/2, h/8, (w/4), (h/64)
                            * 27, text_hidden=True, placeholder_text="password"),
            Button.Button(self, w/3, h/8, (w/4) +
                          1/2*(w/2-w/3), (h/64)*39, text="Login",
                          on_click=lambda:self.login_attempt(self.elements[0].text, self.elements[1].text))
        ]

    def handle_event(self, event):
        [elem.handle_event(event) for elem in self.elements]

    def login_attempt(self, username, password):
        print(f"Username: {username}, Password: {password}")
        self.app.open_menu()

    def tick(self):
        pass

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((20, 20, 20))
        [elem.draw() for elem in self.elements]
