# alien_invasion.py
# Enhanced game loop & utilities for the "Alien Invasion" Pygame project.
# - Graceful shutdown & error-safe init
# - Delta-time based update (with backward-compat fallback)
# - Fullscreen toggle (F11), pause (P), exit (Esc/Q), FPS overlay (F3), screenshot (F12)
# - Resizable window with high-DPI scaling + optional vsync
# - Lightweight starfield background (configurable via Settings if present)
# - Centralized input handling & window utilities
# - Type hints and small quality-of-life helpers

from __future__ import annotations

import sys
import time
import pygame
from typing import List, Tuple

from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets, loop, and behavior."""

    # --------- Key bindings (tweak to taste) ---------
    KEY_QUIT = (pygame.K_ESCAPE, pygame.K_q)
    KEY_TOGGLE_FULLSCREEN = pygame.K_F11
    KEY_TOGGLE_FPS = pygame.K_F3
    KEY_PAUSE = pygame.K_p
    KEY_SCREENSHOT = pygame.K_F12
    KEY_MOVE_RIGHT = pygame.K_RIGHT
    KEY_MOVE_LEFT = pygame.K_LEFT

    # --------- Defaults if not present in Settings ---------
    DEFAULT_FPS = 60
    DEFAULT_BG_COLOR = (30, 30, 40)
    DEFAULT_SCREEN_SIZE = (1200, 800)
    DEFAULT_STAR_COUNT = 90
    DEFAULT_STAR_SPEED_RANGE = (30, 140)  # px/s
    DEFAULT_STAR_SIZE_RANGE = (1, 3)

    def __init__(self) -> None:
        """Game creation and initialization."""
        pygame.init()
        self.clock = pygame.time.Clock()

        # Settings & safe fallbacks
        self.settings = Settings()
        self.framerate: int = getattr(self.settings, "framerate", self.DEFAULT_FPS)
        self.bg_color: Tuple[int, int, int] = getattr(self.settings, "bg_color", self.DEFAULT_BG_COLOR)
        self._base_size: Tuple[int, int] = (
            getattr(self.settings, "screen_width", self.DEFAULT_SCREEN_SIZE[0]),
            getattr(self.settings, "screen_height", self.DEFAULT_SCREEN_SIZE[1]),
        )

        # Window state
        self.is_fullscreen = False
        self._windowed_size = self._base_size
        self._create_window()

        # Draw resources
        self._init_fonts()

        # Entities
        self.ship = Ship(self)

        # Loop state
        self.running = True
        self.paused = False
        self.show_fps = True

        # Background effect
        self._init_starfield()

    # -------------------------------------------------------------------------
    # Initialization helpers
    # -------------------------------------------------------------------------
    def _create_window(self) -> None:
        """Create the game window with resizable + scaled flags and optional vsync."""
        pygame.display.set_caption("Alien Invasion")

        flags = pygame.SCALED | pygame.RESIZABLE
        try:
            # vsync keyword is only supported on newer pygame + drivers
            self.screen = pygame.display.set_mode(self._windowed_size, flags, vsync=1)  # type: ignore[arg-type]
        except TypeError:
            # Fallback if vsync kw not recognized
            self.screen = pygame.display.set_mode(self._windowed_size, flags)
        except Exception:
            # Ultimate fallback: basic window
            self.screen = pygame.display.set_mode(self._windowed_size)
        self.screen_rect = self.screen.get_rect()

        # Optional window icon (place an "icon.png" next to your main module if desired)
        try:
            icon = pygame.image.load("icon.png").convert_alpha()
            pygame.display.set_icon(icon)
        except Exception:
            pass

    def _init_fonts(self) -> None:
        """Initialize fonts for overlays."""
        pygame.font.init()
        # Using default font for portability
        self.font_small = pygame.font.Font(None, 22)

    def _init_starfield(self) -> None:
        """Generate a simple starfield background."""
        import random

        count = getattr(self.settings, "star_count", self.DEFAULT_STAR_COUNT)
        spd_min, spd_max = getattr(self.settings, "star_speed_range", self.DEFAULT_STAR_SPEED_RANGE)
        sz_min, sz_max = getattr(self.settings, "star_size_range", self.DEFAULT_STAR_SIZE_RANGE)

        self._stars: List[dict] = []
        for _ in range(count):
            self._stars.append(
                {
                    "x": random.uniform(0, self.screen_rect.width),
                    "y": random.uniform(0, self.screen_rect.height),
                    "speed": random.uniform(spd_min, spd_max),
                    "size": random.randint(sz_min, sz_max),
                    "color": (200, 200, 220),
                }
            )

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    def run(self) -> None:
        """Start the main executor for the game."""
        try:
            while self.running:
                dt = self.clock.tick(self.framerate) / 1000.0  # seconds
                self._check_events()

                if not self.paused:
                    self._update(dt)

                self._render_screen(dt)
        finally:
            self._shutdown()

    # -------------------------------------------------------------------------
    # Update & Render
    # -------------------------------------------------------------------------
    def _update(self, dt: float) -> None:
        """Update all game objects and background effects."""
        self._update_stars(dt)

        # Call ship update with delta-time if supported, else fallback to no-arg
        try:
            self.ship.update(dt)  # type: ignore[arg-type]
        except TypeError:
            self.ship.update()

    def _update_stars(self, dt: float) -> None:
        """Move stars downward and wrap around."""
        for s in self._stars:
            s["y"] += s["speed"] * dt
            if s["y"] > self.screen_rect.height:
                s["y"] = 0
                s["x"] %= self.screen_rect.width  # keep x within bounds

    def _render_screen(self, dt: float) -> None:
        """Render the frame."""
        self.screen.fill(self.bg_color)
        self._draw_stars()
        self.ship.draw()

        if self.show_fps:
            self._draw_fps_overlay()

        pygame.display.flip()

    def _draw_stars(self) -> None:
        for s in self._stars:
            pygame.draw.rect(
                self.screen,
                s["color"],
                pygame.Rect(int(s["x"]), int(s["y"]), s["size"], s["size"]),
            )

    def _draw_fps_overlay(self) -> None:
        fps = self.clock.get_fps()
        txt = f"FPS: {fps:5.1f}   {'PAUSED' if self.paused else ''}"
        surf = self.font_small.render(txt, True, (220, 220, 230))
        self.screen.blit(surf, (8, 6))

    # -------------------------------------------------------------------------
    # Event handling
    # -------------------------------------------------------------------------
    def _check_events(self) -> None:
        """Respond to keypresses, mouse, and window events."""
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                self.running = False
            elif et == pygame.WINDOWRESIZED:
                self._handle_resize(event)
            elif et == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif et == pygame.KEYUP:
                self._handle_keyup(event)

    def _handle_resize(self, event: pygame.event.Event) -> None:
        """Adjust internal rects on window resize."""
        self.screen_rect = self.screen.get_rect()

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keydown events."""
        key = event.key
        if key in self.KEY_QUIT:
            self.running = False
            return

        if key == self.KEY_TOGGLE_FULLSCREEN:
            self._toggle_fullscreen()
        elif key == self.KEY_TOGGLE_FPS:
            self.show_fps = not self.show_fps
        elif key == self.KEY_PAUSE:
            self.paused = not self.paused
        elif key == self.KEY_SCREENSHOT:
            self._save_screenshot()

        # Movement (delegated to Ship API used in original project)
        elif key == self.KEY_MOVE_RIGHT:
            self.ship.start_moving_right()
        elif key == self.KEY_MOVE_LEFT:
            self.ship.start_moving_left()

    def _handle_keyup(self, event: pygame.event.Event) -> None:
        """Handle keyup events."""
        key = event.key
        if key == self.KEY_MOVE_RIGHT:
            self.ship.stop_moving_right()
        elif key == self.KEY_MOVE_LEFT:
            self.ship.stop_moving_left()

    # -------------------------------------------------------------------------
    # Utilities
    # -------------------------------------------------------------------------
    def _toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed modes."""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Remember windowed size
            self._windowed_size = (self.screen_rect.width, self.screen_rect.height)
            try:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.SCALED)
            except Exception:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Restore previous window size
            flags = pygame.SCALED | pygame.RESIZABLE
            try:
                self.screen = pygame.display.set_mode(self._windowed_size, flags, vsync=1)  # type: ignore[arg-type]
            except TypeError:
                self.screen = pygame.display.set_mode(self._windowed_size, flags)
        self.screen_rect = self.screen.get_rect()

    def _save_screenshot(self) -> None:
        """Save a timestamped screenshot into the current working directory."""
        filename = time.strftime("screenshot_%Y%m%d_%H%M%S.png")
        try:
            pygame.image.save(self.screen, filename)
            print(f"[screenshot] Saved: {filename}")
        except Exception as e:
            print(f"[screenshot] Failed: {e}", file=sys.stderr)

    def _shutdown(self) -> None:
        """Gracefully shutdown pygame & exit."""
        try:
            pygame.quit()
        finally:
            # Exit with 0 code for a normal quit.
            sys.exit(0)


if __name__ == "__main__":
    game = AlienInvasion()
    game.run()
