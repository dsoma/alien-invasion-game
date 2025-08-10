# ship.py
# Improved Ship class for Pygame:
# - Frame-rate independent movement (dt)
# - Smooth acceleration/deceleration with friction
# - Subpixel accuracy using Vector2
# - Rotation "tilt" feedback while strafing
# - Robust image loading with alpha/colorkey fallback
# - Resizable-window aware (anchors to bottom)
# - Optional invincibility blink
# - Pixel mask for precise collisions
# - Clean start/stop movement API (backward compatible)

from __future__ import annotations

import os
import pygame
from typing import Optional, Tuple


class Ship:
    """A class to manage the player ship."""

    # Reasonable defaults if not found in Settings
    _DEFAULT_SPEED_PPS = 480.0        # pixels per second (max horizontal speed)
    _DEFAULT_ACCEL_PPS2 = 1800.0      # horizontal acceleration
    _DEFAULT_FRICTION = 8.0           # higher = faster slow down
    _DEFAULT_TILT_MAX = 10.0          # degrees of tilt at max speed
    _DEFAULT_BOTTOM_MARGIN = 24       # pixels from screen bottom

    def __init__(self, game) -> None:
        """Initialize the ship and set its starting position."""
        # References
        self.game = game
        self.screen: pygame.Surface = game.screen
        self.settings = game.settings

        # Pull configurable values (with safe fallbacks)
        self.max_speed: float = float(getattr(self.settings, "ship_speed", self._DEFAULT_SPEED_PPS))
        self.accel: float = float(getattr(self.settings, "ship_accel", self._DEFAULT_ACCEL_PPS2))
        self.friction: float = float(getattr(self.settings, "ship_friction", self._DEFAULT_FRICTION))
        self.tilt_max: float = float(getattr(self.settings, "ship_tilt_max", self._DEFAULT_TILT_MAX))
        self.bottom_margin: int = int(getattr(self.settings, "ship_bottom_margin", self._DEFAULT_BOTTOM_MARGIN))
        self.image_path: str = getattr(self.settings, "ship_image", "images/ship_sky_blue.bmp")

        # Load sprite (robustly)
        self.base_image: pygame.Surface = self._load_image(self.image_path)
        self.image: pygame.Surface = self.base_image.copy()
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

        # Use mid-bottom as our anchor (keeps feet on the same line when rotating)
        self.rect: pygame.Rect = self.image.get_rect()
        self.pos = pygame.Vector2(0.0, 0.0)  # midbottom position (float)
        self.vel = pygame.Vector2(0.0, 0.0)  # velocity (px/s)

        # Movement flags (compatible with your existing input handling)
        self.moving_right = False
        self.moving_left = False

        # Visual/logic helpers
        self._base_half_width = self.base_image.get_width() * 0.5
        self._invincible_until_ms: int = 0
        self._blink_hz: float = 8.0

        # Initial placement
        self.center()

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def center(self) -> None:
        """Center the ship at the bottom of the current screen."""
        screen_rect = self.game.screen.get_rect()
        self.pos.xy = (screen_rect.centerx, screen_rect.bottom - self.bottom_margin)
        self._apply_transform()

    def start_moving_right(self) -> None:
        self.moving_right = True

    def start_moving_left(self) -> None:
        self.moving_left = True

    def stop_moving_right(self) -> None:
        self.moving_right = False

    def stop_moving_left(self) -> None:
        self.moving_left = False

    def set_invincible(self, seconds: float) -> None:
        """Temporarily make the ship blink (non-collidable can be handled by game)."""
        self._invincible_until_ms = pygame.time.get_ticks() + int(max(0.0, seconds) * 1000)

    def is_invincible(self) -> bool:
        return pygame.time.get_ticks() < self._invincible_until_ms

    def get_collision_mask(self) -> pygame.Mask:
        """Return a pixel mask for precise collisions."""
        return self.mask

    # --------------------------------------------------------------------- #
    # Main loop hooks
    # --------------------------------------------------------------------- #
    def update(self, dt: float = 0.0) -> None:
        """
        Update the ship's state.
        :param dt: Delta time in seconds (frame-rate independent). If 0, will
                   fallback to the game's clock time implicitly (not ideal).
        """
        # Ensure we keep hugging the bottom even on resizes
        screen_rect = self.game.screen.get_rect()
        self.pos.y = screen_rect.bottom - self.bottom_margin

        # Fallback if dt not provided
        if dt <= 0.0:
            dt = max(1e-6, self.game.clock.get_time() / 1000.0)

        # Horizontal input → acceleration
        if self.moving_right ^ self.moving_left:
            # Only one of them is true
            if self.moving_right:
                self.vel.x += self.accel * dt
            elif self.moving_left:
                self.vel.x -= self.accel * dt
        else:
            # Apply friction towards 0 when no (or both) inputs
            self.vel.x *= max(0.0, 1.0 - self.friction * dt)

        # Clamp to max speed
        self.vel.x = max(-self.max_speed, min(self.vel.x, self.max_speed))

        # Integrate position (subpixel)
        self.pos.x += self.vel.x * dt

        # Keep mid-bottom within the horizontal bounds (using base width to avoid jitter on rotation)
        left_bound = self._base_half_width
        right_bound = screen_rect.width - self._base_half_width
        self.pos.x = max(left_bound, min(right_bound, self.pos.x))

        # Apply visual transform (rotation tilt) and update rect/mask
        self._apply_transform()

    def draw(self) -> None:
        """Draw the ship at its current location with optional invincibility blink."""
        if self.is_invincible():
            # Simple blink: skip draw every other phase
            phase_ms = int(1000 / (self._blink_hz * 2))
            if (pygame.time.get_ticks() // phase_ms) % 2 == 0:
                return  # invisible this frame
        self.game.screen.blit(self.image, self.rect)

    # --------------------------------------------------------------------- #
    # Internals
    # --------------------------------------------------------------------- #
    def _apply_transform(self) -> None:
        """Rotate sprite based on velocity and place it by midbottom anchor."""
        # Tilt proportional to horizontal velocity (small angle for a subtle feel)
        if self.max_speed > 0:
            angle = -self.tilt_max * (self.vel.x / self.max_speed)
        else:
            angle = 0.0

        # Rotate without scaling for crisp pixels (use rotozoom if you want scale effects)
        rotated: pygame.Surface = pygame.transform.rotozoom(self.base_image, angle, 1.0)
        midbottom = (int(round(self.pos.x)), int(round(self.pos.y)))

        # Update image, rect, and mask (pixel-perfect collisions)
        self.image = rotated
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.mask = pygame.mask.from_surface(self.image)

    def _load_image(self, path: str) -> pygame.Surface:
        """Load an image robustly, falling back to a simple placeholder if missing."""
        surf: Optional[pygame.Surface] = None

        # Try exact path
        if os.path.isfile(path):
            try:
                # Prefer per-pixel alpha if available
                loaded = pygame.image.load(path)
                surf = loaded.convert_alpha() if loaded.get_alpha() is not None else loaded.convert()
                # If it's not alpha-based (e.g., BMP), try colorkey from the top-left pixel
                if surf.get_alpha() is None:
                    colorkey = surf.get_at((0, 0))
                    surf.set_colorkey(colorkey)
            except Exception:
                surf = None

        if surf is None:
            # Fallback placeholder
            surf = pygame.Surface((64, 48), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))
            pygame.draw.polygon(
                surf,
                (120, 200, 255),
                [(4, 44), (32, 4), (60, 44)],
                width=0,
            )
            pygame.draw.polygon(
                surf,
                (40, 80, 120),
                [(10, 44), (32, 12), (54, 44)],
                width=2,
            )

        return surf
