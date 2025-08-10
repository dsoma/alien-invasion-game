import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Alien object."""

    def __init__(self, game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.alien.image)
        self.rect  = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)