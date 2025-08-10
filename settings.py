class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (135, 206, 235)
        self.framerate = 60
        self.speed = 2.5
        self.step_size = 3
