import pygame

from pygame.sprite import Sprite

class BulletGroup(Sprite):
    """A group of bullets."""

    def __init__(self, game):
        """Initialize the bullet group."""
        super().__init__()
        self.game = game
        self.bullets = pygame.sprite.Group()


    def fire(self):
        """Add a bullet to the group and fire it."""
        if len(self.bullets) < self.game.settings.bullet.max_bullets:
            self.bullets.add( Bullet(self.game) )


    def update(self):
        """Update the position of the bullets."""
        for bullet in self.bullets.sprites():
            bullet.update()

        # Cleanup bullets that are off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def draw(self):
        """Draw the bullets."""
        for bullet in self.bullets.sprites():
            bullet.draw()



class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game):
        """Initialize the bullet and set its starting position."""
        super().__init__()

        self.game     = game
        self.settings = game.settings
        self.screen   = game.screen
        self.color    = self.settings.bullet.color
        self.rect     = pygame.Rect(0, 0,
                                    self.settings.bullet.width,
                                    self.settings.bullet.height)

        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.firing = False


    def update(self):
        """Updates the position of the bullet."""
        self.y -= self.settings.bullet.speed
        self.rect.y = self.y


    def draw(self):
        """Renders the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


    def fire(self):
        """Fires the bullet."""
        self.rect.midtop = self.game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.firing = True


    def stop_firing(self):
        """Stops the bullet from firing."""
        self.firing = False