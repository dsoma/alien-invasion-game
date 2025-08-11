import pygame
from pygame.sprite import Sprite

class AlienFleet(Sprite):
    """A fleet of aliens."""

    def __init__(self, game):
        """Initialize the alien fleet."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.aliens = pygame.sprite.Group()
        self.screen_width  = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height


    def build(self):
        """Build the fleet of aliens."""
        alien = Alien(self.game)
        alien_width, alien_height = alien.rect.size
        x, y = alien_width, alien_height
        alien.x = alien_width

        while y < (self.screen_height - 3 * alien_height):
            while x < (self.screen_width - 2 * alien_width):
                self._create_alien(x, y)
                x += 2 * alien_width

            x = alien_width
            y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and add it to the fleet."""
        new_alien = Alien(self.game)
        new_alien.x = x_position
        new_alien.y = y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def draw(self):
        """Draw the fleet of aliens."""
        self.aliens.draw(self.screen)


class Alien(Sprite):
    """Alien object."""

    def __init__(self, game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.game = game
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.alien.image)
        self.rect  = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
