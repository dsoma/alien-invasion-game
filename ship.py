import pygame

class Ship:
    """A class to manage the space ship."""

    def __init__(self, game):
        """Init the ship and set its starting position."""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # load the ship image
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Place the ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)



