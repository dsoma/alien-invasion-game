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
        self._create_fullscreen_window()
        self.ship = Ship(self)


    def run(self):
        """Start the main executor for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._render_screen()
            self.clock.tick(self.settings.framerate)


    def _create_fullscreen_window(self):
        """Create the game window."""
        pygame.display.set_caption('Alien Invasion')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width  = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height


    def _create_normal_window(self):
        """Create the game window."""
        pygame.display.set_caption('Alien Invasion')
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event)


    def _render_screen(self):
        """Render the screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.draw()
        pygame.display.flip()


    def _handle_keydown(self, event):
        """Handle keydown events."""
        if event.key == pygame.K_RIGHT:
            self.ship.start_moving_right()
        elif event.key == pygame.K_LEFT:
            self.ship.start_moving_left()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()


    def _handle_keyup(self, event):
        """Handle keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.stop_moving_right()
        elif event.key == pygame.K_LEFT:
            self.ship.stop_moving_left()


if __name__ == "__main__":
    game = AlienInvasion()
    game.run()
