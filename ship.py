"""A ship for Alien Invasion."""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to work with a ship."""

    def __init__(self, game):
        """Initialize the ship."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the ship image and set its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()

        # Place the ship at the bottom center.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's center.
        self.x = float(self.rect.x)

        # Movement flag.
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update the position based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
