
class Stats:
    """Track statistics for Alien Invasion Game."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship.limit
        self.score = 0
        self.level = 1
        self.high_score = 0

