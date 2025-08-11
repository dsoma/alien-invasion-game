
class Stats:
    """Track statistics for Alien Invasion Game."""

    def __init__(self, game):
        """Initialize statistics."""
        self.settings = game.settings
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship.limit
        self.score = int(0)
        self.level = 1
        self.update_count = 0


    def add_score(self, points):
        """Add points to the score."""
        self.score += int(points)
        self.score = max(self.score, 0)


    def game_over(self):
        """Game over."""
        self.high_score = max(self.high_score, self.score)
        self.level = 1
        self.ships_left = self.settings.ship.limit

