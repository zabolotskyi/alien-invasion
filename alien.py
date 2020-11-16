"""An alien for Alien Invasion."""
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to work with an alien."""

    def __init__(self, screen, settings):
        """Initialize the alien."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Load the alien image and set its rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Place the alien at the top left corner.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a decimal value for the alien's x position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()

        if self.rect.x + self.rect.width >= screen_rect.right:
            return True
        elif self.rect.x <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
