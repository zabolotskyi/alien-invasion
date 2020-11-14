"""A ship for Alien Invasion."""
import pygame


class Ship:
    """A class to work with a ship."""

    def __init__(self, screen, settings):
        """Initialize the ship."""
        self.screen = screen
        self.settings = settings

        # Load the ship image and set its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Place the ship at the bottom center.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.width / 2
        self.rect.bottom = self.screen_rect.height

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag.
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """Update the position based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
