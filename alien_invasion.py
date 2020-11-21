"""Alien Invasion game."""
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from button import Button

import game_fuctions as gf


def run_game():
    """Main game function."""
    # Initialize pygame, settings and screen object.
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode(
        (
            settings.screen_width,
            settings.screen_height,
        )
    )
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(screen, settings, "Play")

    # Create an instance of game stats.
    stats = GameStats(settings)

    # Make a scoreboard.
    sb = Scoreboard(screen, settings, stats)

    # Make a ship.
    ship = Ship(screen, settings)

    # Make a group of bullets.
    bullets = Group()

    # Make a group of aliens.
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(screen, settings, ship, aliens)

    # Start the main loop for the game.
    while True:
        gf.update_screen(
            screen,
            settings,
            stats,
            sb,
            play_button,
            ship,
            aliens,
            bullets,
        )

        gf.check_events(
            screen,
            settings,
            stats,
            sb,
            play_button,
            ship,
            aliens,
            bullets,
        )

        if stats.game_active:
            ship.update()

            gf.update_bullets(
                screen,
                settings,
                stats,
                sb,
                ship,
                aliens,
                bullets,
            )

            gf.update_aliens(
                screen,
                settings,
                stats,
                sb,
                ship,
                aliens,
                bullets,
            )

            gf.update_screen(
                screen,
                settings,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
            )


run_game()
