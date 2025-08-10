import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Game creation and initialization."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)

    def run(self):
        """Start the main executor for the game."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()

            self.screen.fill(self.settings.bg_color)
            self.ship.draw()
            pygame.display.flip()
            self.clock.tick(self.settings.framerate)

if __name__ == "__main__":
    game = AlienInvasion()
    game.run()
