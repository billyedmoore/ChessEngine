import pygame

from . import TextBox, Button


class RegistrationScreen(pygame.Surface):
    """
    Screen showed to users allowing them to register a new account.
    """

    def __init__(self, app, w, h):
        """
        Instantiate the registation screen

        Parameters:
            App app - the "app" object this screen in contained within
            int w - the width of the 'screen'(the window) in pixels
            int h - the height od the 'screen'(the window) in pixels

        """
        pygame.Surface.__init__(self, size=(w, h))
        self.surface = app.screen
        self.app = app
        self.elements = [TextBox.TextBox(self, w/2, h/7, w/4, (h/49)*4,
                                         placeholder_text="username"),
                         TextBox.TextBox(self, w/2, h/7, w/4, (h/49)*12,
                                         placeholder_text="email@chessgame.org"),
                         TextBox.TextBox(self, w/2, h/7, w/4, (h/49) * 20,
                                         placeholder_text="password", text_hidden=True),
                         TextBox.TextBox(self, w/2, h/7, w/4, (h/49) * 28,
                                         placeholder_text="confirm password", text_hidden=True),
                         Button.Button(self, w/3, h/7,
                                       (w/4+int(1/2 * (w/2-w/3))),
                                       (h/49) * 36, text="register",
                                       on_click=lambda:self.registation_attempt(
                                           self.elements[0].text,
                                           self.elements[1].text,
                                           self.elements[2].text,
                                           self.elements[3].text
                                       ))]

    def handle_event(self, event):
        """
        Passes events taking place to the elements (TextBox and Button objects)
        so they can handle them (e.g. hover for Buttons and focus for TextBoxs)

        Parameters:
            pygame.event event - the event to be handled
        """
        [elem.handle_event(event) for elem in self.elements]

    def registation_attempt(self, username, email, password_one, password_two):
        """
        Attempt to register a user using the values currently in the text boxes

        Parameters:
            str username - 
            str email -
            str password_one - the password entered in to the "password" 
                               text box 
            str password_two - the password entered in to the "confirm 
                               password" text box, should be the same
        Return Values:
            None
        """
        success, reason = self.app.client.register(
            username, email, password_one, password_two)
        if success:
            self.app.open_login_screen()
        else:
            errors = [False, False, False, False]
            if reason == "email":
                errors[1] = True
            elif reason == "password":
                errors[2] = True
                errors[3] = True
            elif reason == "username":
                errors[0] = True
            elif reason == "exists":
                errors = [True for i in range(4)]

            for i in range(4):
                self.elements[i].set_error(errors[i])

    def tick(self):
        """
        Execututed on every game loop, no action is performed currently
        """
        pass

    def draw(self):
        """
        Draw the 'screen' to the display.
        """
        self.surface.blit(self, (0, 0))
        self.fill((255, 255, 255))
        [elem.draw() for elem in self.elements]
