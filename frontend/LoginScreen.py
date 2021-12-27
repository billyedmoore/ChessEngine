import pygame
from client_side.User import User
from . import TextBox, Button


class LoginScreen(pygame.Surface):
    def __init__(self, app, w, h):
        pygame.Surface.__init__(self, size=(w, h))
        self.surface = app.screen
        self.app = app
        self.elements = [
            TextBox.TextBox(self, w/2, h/7, (w/4), (h/49)*7,
                            placeholder_text="username", text="billyedmoore"),
            TextBox.TextBox(self, w/2, h/7, (w/4), (h/49)*16,
                            text_hidden=True, placeholder_text="password",
                            text="password"),
            # , text="password"),
            Button.Button(self, w/3, h/7, (w/4) +
                          1/2*(w/2-w/3), (h/49)*26, text="login",
                          on_click=lambda:self.login_attempt(self.elements[0].text, self.elements[1].text)),
            Button.Button(self, w/3, h/7, (w/4) + 1/2 *
                          (w/2-w/3), (h/49)*35, text="register",
                          on_click=lambda:self.app.open_registration_screen())

        ]

    def handle_event(self, event):
        [elem.handle_event(event) for elem in self.elements]

    def login_attempt(self, username, password):
        print(f"Username: {username}, Password: {password}")
        user = User.login(self.app.client, username, password)

        if user:
            self.app.handle_login(user)
        else:
            self.elements[0].set_error(True)
            self.elements[1].set_error(True)

    def load_register_screen(self):
        print("That dont exist you knob")

    def tick(self):
        pass

    def draw(self):
        self.surface.blit(self, (0, 0))
        self.fill((255, 255, 255))
        [elem.draw() for elem in self.elements]
