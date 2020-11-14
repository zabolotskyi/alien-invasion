"""Alien Invasion game."""
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_fuctions as gf


def run_game():
    """Main game function."""
    # Initialize pygame, settings and screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make a ship.
    ship = Ship(screen, settings)
    # Make a bullets group.
    bullets = Group()

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(screen, bullets)
        gf.update_screen(settings, screen, ship, bullets)


run_game()
