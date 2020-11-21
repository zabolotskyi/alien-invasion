"""A class to store game statistics and reset it."""


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.game_active = False
        self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """Reset the stats to default values."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
