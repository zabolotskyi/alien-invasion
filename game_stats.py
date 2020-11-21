"""A class to store game statistics and reset it."""
import json

from consts import game_stats_file


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.game_active = False
        high_score = self.retrieve_high_score()
        self.high_score = high_score

        self.reset_stats()

    def retrieve_high_score(self):
        try:
            with open(game_stats_file) as file:
                high_score = json.load(file)
        except FileNotFoundError:
            return 0
        else:
            return high_score

    def reset_stats(self):
        """Reset the stats to default values."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
