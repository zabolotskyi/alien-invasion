"""Alien Invasion game."""
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_fuctions as gf


def run_game():
    """Main game function."""
    # Initialize pygame, settings and screen object.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance of game stats.
    stats = GameStats(settings)

    # Make a ship.
    ship = Ship(screen, settings)
    # Make a group of bullets.
    bullets = Group()
    # Make a group of aliens.
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(screen, settings, aliens, ship)

    # Start the main loop for the game.
    while True:
        gf.check_events(settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(screen, settings, aliens, ship, bullets)
            gf.update_aliens(screen, settings, ship, aliens, bullets, stats)
            gf.update_screen(settings, screen, ship, aliens, bullets)


run_game()
