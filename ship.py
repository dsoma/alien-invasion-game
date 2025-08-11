import pygame

class Ship:
    """A class to manage the space ship."""

    def __init__(self, game):
        """Init the ship and set its starting position."""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.bottom_bar = game.bottom_bar

        # load the ship image
        self.image  = pygame.image.load(self.settings.ship.image)
        self.rect   = self.image.get_rect()
        self.width  = self.rect.width
        self.height = self.rect.height

        # Place the ship at the bottom center of the screen
        self.center_ship()

        self.moving_right = False
        self.moving_left  = False


    def draw(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


    def update(self):
        """Update the ship's position."""
        if self.moving_right:
            self.x += self.settings.ship.speed * self.settings.ship.step_size
            self.x  = min(self.x, self.screen_rect.right - self.width)
        if self.moving_left:
            self.x -= self.settings.ship.speed * self.settings.ship.step_size
            self.x  = max(self.x, 0)

        self.rect.x = self.x


    def start_moving_right(self):
        """Ship is moving right."""
        self.moving_right = True


    def start_moving_left(self):
        """Ship is moving left."""
        self.moving_left = True


    def stop_moving_right(self):
        """Ship stopped moving right."""
        self.moving_right = False


    def stop_moving_left(self):
        """Ship stopped moving left."""
        self.moving_left = False


    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.bottom_bar.rect.midtop
        self.x = float(self.rect.x)


    def hit(self):
        """Ship hit by an alien."""
        print("Ship hit by an alien.")


