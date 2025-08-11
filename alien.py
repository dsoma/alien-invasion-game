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
        self.ship = game.ship
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


    def update(self):
        """Update the alien's position."""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_if_hit_ship()
        self._did_aliens_reach_bottom(self.screen.get_rect())


    def clear(self):
        """Clear the aliens."""
        self.aliens.empty()


    def _check_fleet_edges(self):
        """Check if any aliens have reached the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien.drop_speed
        self.settings.alien.direction *= -1


    def is_empty(self):
        """Check if the fleet is empty."""
        return len(self.aliens) == 0



    def _check_if_hit_ship(self):
        """Check for collisions between aliens and ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.game.ship_hit()


    def _did_aliens_reach_bottom(self, screen_rect):
        """Did the aliens in the group reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.game.aliens_hit_bottom()


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


    def check_edges(self):
        """Check if the alien is at the edge of the screen."""
        screen_rect = self.game.screen.get_rect()
        return (self.rect.right >= screen_rect.right or self.rect.left <= 0)



    def update(self):
        """Update the alien's position."""
        self.x += self.settings.alien.speed * self.settings.alien.direction
        self.rect.x = self.x
