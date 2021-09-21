import pygame
import os


class Piece(pygame.sprite.Sprite):
    _pos = (0, 0)

    def __init__(self, number, pos, square_width, piece_letter, piece_colour):
        self.number = number
        self.pos = pos
        self.in_position = True
        pygame.sprite.Sprite.__init__(self)
        self._piece_letter = piece_letter.lower() if piece_colour.lower(
        ) == "b" else piece_letter.upper()
        self.colour = piece_colour.lower()
        self.square_width = int(square_width)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        # if pos[0] in range(8) and pos[1] in range(8):
        self._pos = pos

    @property
    def piece_letter(self):
        return self._piece_letter

    @piece_letter.setter
    def piece_letter(self, piece_letter):
        self._piece_letter = piece_letter.lower() if self.colour.lower(
        ) == "b" else piece_letter.upper()

    def update(self):
        self.rect = (self.pos[1] * self.square_width,
                     self.pos[0] * self.square_width, self.square_width, self.square_width)
        self.piece_image = pygame.image.load(
            os.path.join("frontend", "image", f"{self.piece_letter.lower()}_{self.colour.lower()}.svg"))
        self.piece_image = pygame.transform.scale(self.piece_image, (self.square_width, self.square_width))
        self.image = pygame.Surface(
            [self.square_width, self.square_width], pygame.SRCALPHA, 32)
        rect = self.piece_image.get_rect(
            center=(self.square_width / 2, self.square_width / 2))
        self.image.blit(self.piece_image, rect)
