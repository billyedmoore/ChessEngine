import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN
from time import sleep


class SimpleTextScreen(pygame.Surface):

    def __init__(self, app, w, h,
                 heading_text="Heading",
                 body_text=[
                     "This is body text.",
                     "This is another line of body text."],
                 big_font=None,
                 small_font=None
                 ):
        """
        Instantiate the TextScreen
        """
        pygame.Surface.__init__(self, size=(w, h))
        self.surface = app.screen
        self.app = app
        self.w = w
        self.h = h
        self.heading_text = heading_text
        self.body_text = body_text
        self.big_font = big_font if big_font else pygame.font.SysFont(
            "freemono", 40)
        self.small_font = small_font if big_font else pygame.font.SysFont(
            "freemono", 20)

    def handle_event(self, event):
        """
        Handle the events happening on the screen, by default do nothing 
        with it. This will be overwritten by the sub classes

        Parameters:
            pygame.event event - The event that is taking place in the program
        """
        pass

    def tick(self):
        """
        Runs once per loop but does nothing by default
        """
        pass

    def draw(self):
        """
        Draw the text to the screen. Called often so should be reasonably 
        efficient.

        (Added coments as is not 100% clear)
        """
        # draw self on the app screen
        self.surface.blit(self, (0, 0))

        # fill with white
        self.fill((255, 255, 255))

        # reder the heading "Game Over" usually
        heading_surface = self.big_font.render(
            self.heading_text, 1, (20, 20, 20))
        body_height = 0

        for count, line in enumerate(self.body_text):
            body_surf = (self.small_font.render(
                line, 1, (20, 20, 20)
            ))
            body_height = body_surf.get_height()
            # get rect for position of line
            body_rect = body_surf.get_rect(
                center=(self.w/2, self.h/2+body_height*count))
            # draw line to screen
            self.blit(body_surf, body_rect)

        # get the rect for the heading when the center in the center -
        # the space where the body text is
        heading_rect = heading_surface.get_rect(
            center=(self.w/2,
                    self.h/2-2*(body_height)))

        # draw heading to screen
        self.blit(heading_surface, heading_rect)
