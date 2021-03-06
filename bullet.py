"""A bullet that is shot by the ship."""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = game.screen

        # Create a bullet rect at (0, 0) and correct the position.
        self.rect = pygame.Rect(
            0, 0, game.settings.bullet_width, game.settings.bullet_height
        )
        self.rect.midtop = game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

        self.color = game.settings.bullet_color
        self.speed_factor = game.settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
