import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import BulletGroup
from alien import AlienFleet
from stats import Stats
from button import Button

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Game creation and initialization."""
        pygame.init()
        self.game_in_progress = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self._create_fullscreen_window()
        self.stats = Stats(self)
        self.play_button = Button(self, "Play")
        self.ship = Ship(self)
        self.bullets = BulletGroup(self)
        self.aliens = AlienFleet(self)
        self._create_fleet()


    def run(self):
        """Start the main executor for the game."""
        while True:
            self._check_events()

            if self.game_in_progress:
                self.ship.update()
                self.bullets.update()
                self._recreate_fleet_if_empty()
                self.aliens.update()

            self._render_screen()
            self.clock.tick(self.settings.screen.framerate)


    def _create_fullscreen_window(self):
        """Create the game window."""
        pygame.display.set_caption('Alien Invasion')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen.width  = self.screen.get_rect().width
        self.settings.screen.height = self.screen.get_rect().height


    def _create_normal_window(self):
        """Create the game window."""
        pygame.display.set_caption('Alien Invasion')
        self.screen = pygame.display.set_mode((
            self.settings.screen.width,
            self.settings.screen.height
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _render_screen(self):
        """Render the screen."""
        self.screen.fill(self.settings.screen.bg_color)

        if not self.game_in_progress:
            self.play_button.draw()
        else:
            self.ship.draw()
            self.bullets.draw()
            self.aliens.draw()

        pygame.display.flip()


    def _handle_keydown(self, event):
        """Handle keydown events."""
        if event.key == pygame.K_RIGHT:
            self.ship.start_moving_right()
        elif event.key == pygame.K_LEFT:
            self.ship.start_moving_left()
        elif event.key == pygame.K_SPACE:
            self.bullets.fire()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()


    def _handle_keyup(self, event):
        """Handle keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.stop_moving_right()
        elif event.key == pygame.K_LEFT:
            self.ship.stop_moving_left()


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_in_progress:
            self._start_game()


    def _start_game(self):
        """Start a new game."""
        self.stats.reset_stats()
        self.game_in_progress = True
        self.aliens.clear()
        self.bullets.clear()
        self._create_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        self.aliens.build()


    def _recreate_fleet_if_empty(self):
        """Recreate the fleet if it is empty."""
        if self.aliens.is_empty():
            self.bullets.clear()
            self._create_fleet()


    def ship_hit(self):
        """Respond to the ship being hit by an alien."""
        self.stats.ships_left -= 1

        if self.stats.ships_left > 0:
            self.bullets.clear()
            self.aliens.clear()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            sleep(1.0)

        else:
            self.game_over()



    def aliens_hit_bottom(self):
        """One of the aliens has reached the bottom of the screen."""
        # The game behavior is same as when the ship is hit by an alien.
        self.ship_hit()


    def game_over(self):
        """Game over."""
        self.game_in_progress = False
        pygame.mouse.set_visible(True)


if __name__ == "__main__":
    game = AlienInvasion()
    game.run()
