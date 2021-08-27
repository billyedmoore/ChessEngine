import pygame


class Piece(pygame.sprite.Sprite):
    _pos = (0, 0)

    def __init__(self, number, pos, square_width, piece_letter, piece_colour):
        self.number = number
        self.pos = pos
        pygame.sprite.Sprite.__init__(self)
        self.letter = piece_letter.lower() if piece_colour.lower(
        ) == "b" else piece_letter.upper()
        self.colour = piece_colour.lower()
        self.square_width = square_width
        self.rect = (pos[1]*square_width, pos[0] *
                     square_width, square_width, square_width)
        self.image = pygame.Surface(
            [square_width, square_width], pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.piece_image = pygame.image.load(
            f"frontend/image/{self.letter}.svg")
        self.image.blit(self.piece_image, (0, 0))

    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)
        self.image.blit(self.piece_image, (0, 0))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        # if pos[0] in range(8) and pos[1] in range(8):
        self._pos == pos

    def update(self):
        self.rect = (self.pos[1]*self.square_width,
                     self.pos[0]*self.square_width, self.square_width, self.square_width)
