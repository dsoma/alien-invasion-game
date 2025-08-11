
# Settings that change every level are:
# Bullet: width, speed, max_bullets, pass_through
# Ship: speed, step_size
# Alien: speed, drop_speed, points

class BulletSettings:
    """A class to store settings for bullets."""

    def __init__(self):
        """Initialize the bullet settings."""
        self.speed  = 10
        self.width  = 30
        self.height = 15
        self.color  = (60, 60, 60)
        self.max_bullets = 2
        self.pass_through = False
        self.points = -1


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
        self.points = 10


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen = ScreenSettings()
        self.ship   = ShipSettings()
        self.bullet = BulletSettings()
        self.alien  = AlienSettings()
        self.game_speed = 1.0
        self.time_penalty = -1


    def reset_settings(self):
        """Reset the settings to the level = 1 settings."""
        self.game_speed = 1.0
        self.bullet.width = 30
        self.bullet.speed = 10
        self.bullet.max_bullets = 2
        self.bullet.pass_through = False
        self.alien.speed = 1.0
        self.alien.drop_speed = 2.0
        self.ship.speed = 2.5
        self.time_penalty = -1
        self.alien.points = 10
        self.bullet.points = -1

    def level_up(self, level):
        """Level up the settings."""

        # Increase the level and the game speed.
        self.game_speed += 0.2
        self.time_penalty -= 1

        self.bullet.width -= 5
        self.bullet.width = max(self.bullet.width, 3)
        self.bullet.speed *= self.game_speed
        self.bullet.max_bullets += 1
        if level <= 3:
            self.bullet.pass_through = False
        else:
            self.bullet.pass_through = True
            self.bullet.points = -2

        self.alien.speed += 1
        self.alien.drop_speed *= self.game_speed
        self.alien.drop_speed = min(self.alien.drop_speed, 25.0)
        self.alien.points += 2

        self.ship.speed *= self.game_speed
        self.ship.speed = min(self.ship.speed, 17.0)

        print("--------------------------------")
        print(f"Level {level} settings:")
        print(f"Game speed: {self.game_speed}")
        print(f"""  Bullet:
                    width={self.bullet.width},
                    speed={self.bullet.speed},
                    max_bullets={self.bullet.max_bullets},
                    pass_through={self.bullet.pass_through}""")
        print(f"""  Alien:
                    speed={self.alien.speed},
                    drop_speed={self.alien.drop_speed}""")
        print(f"""  Ship:
                    speed={self.ship.speed}""")
        print(f"Current score: {self.stats.score}")
        print(f"Current high score: {self.stats.high_score}")
        print("--------------------------------")
