class BulletSettings:
    """A class to store settings for bullets."""

    def __init__(self):
        """Initialize the bullet settings."""
        self.speed  = 10
        self.width  = 30
        self.height = 15
        self.color  = (60, 60, 60)
        self.max_bullets = 2
        self.pass_through = True


class ShipSettings:
    """Settings for the ship."""

    def __init__(self):
        """Initialize the ship settings."""
        self.speed = 2.5
        self.step_size = 3
        self.limit = 3
        self.image = 'images/ship_sky_blue.bmp'


class ScreenSettings:
    """Settings for the screen."""

    def __init__(self):
        """Initialize the screen settings."""
        self.width     = 1280
        self.height    = 720
        self.bg_color  = (135, 206, 235)
        self.framerate = 60


class AlienSettings:
    """Settings for the aliens."""

    def __init__(self):
        """Initialize the alien settings."""
        self.speed = 1.0
        self.direction = 1 # 1 means right; -1 means left
        self.image = 'images/alien_1.bmp'
        self.drop_speed = 2.0


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen = ScreenSettings()
        self.ship   = ShipSettings()
        self.bullet = BulletSettings()
        self.alien  = AlienSettings()
