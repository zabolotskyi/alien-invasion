"""Alien Invasion game."""
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from button import Button
from bullet import Bullet

import game_fuctions as gf


class AlienInvasion:
    # Overall class to manage the game.

    def __init__(self):
        # Initialize pygame, settings and screen object.
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width,
                self.settings.screen_height,
            )
        )

        # Fullscreen mode.
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Make the Play button.
        self.play_button = Button(self.screen, self.settings, "Play")

        # Create an instance of game stats.
        self.stats = GameStats(self.settings)

        # Make a scoreboard.
        self.sb = Scoreboard(self.screen, self.settings, self.stats)

        # Make a ship.
        self.ship = Ship(self.screen, self.settings)

        # Make a group of bullets.
        self.bullets = Group()

        # Make a group of aliens.
        self.aliens = Group()

        # Create the fleet of aliens.
        gf.create_fleet(self.screen, self.settings, self.ship, self.aliens)

    def run_game(self):
        # Start the main loop for the game.
        while True:
            self._update_screen(
                self.screen,
                self.settings,
                self.stats,
                self.sb,
                self.play_button,
                self.ship,
                self.aliens,
                self.bullets,
            )

            self._check_events(
                self.screen,
                self.settings,
                self.stats,
                self.sb,
                self.play_button,
                self.ship,
                self.aliens,
                self.bullets,
            )

            if self.stats.game_active:
                self.ship.update()

                self._update_bullets(
                    self.screen,
                    self.settings,
                    self.stats,
                    self.sb,
                    self.ship,
                    self.aliens,
                    self.bullets,
                )

                gf.update_aliens(
                    self.screen,
                    self.settings,
                    self.stats,
                    self.sb,
                    self.ship,
                    self.aliens,
                    self.bullets,
                )

                self._update_screen(
                    self.screen,
                    self.settings,
                    self.stats,
                    self.sb,
                    self.play_button,
                    self.ship,
                    self.aliens,
                    self.bullets,
                )

    def _check_events(
        self,
        screen,
        settings,
        stats,
        sb,
        play_button,
        ship,
        aliens,
        bullets,
    ):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gf.store_high_score(stats.high_score)
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(
                    event,
                    screen,
                    settings,
                    stats,
                    ship,
                    sb,
                    aliens,
                    bullets,
                )

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event, ship)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                gf.check_play_button(
                    screen,
                    settings,
                    stats,
                    sb,
                    play_button,
                    ship,
                    aliens,
                    bullets,
                    mouse_x,
                    mouse_y,
                )

    def _update_screen(
        self,
        screen,
        settings,
        stats,
        sb,
        play_button,
        ship,
        aliens,
        bullets,
    ):
        """Handle screen redraws."""
        # Redraw the screen.
        self.screen.fill(settings.bg_color)

        # Redraw all bullets behind the ship and aliens.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(screen)

        # Draw scores.
        self.sb.show_score()

        # Draw a play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_keydown_events(
        self,
        event,
        screen,
        settings,
        stats,
        ship,
        sb,
        aliens,
        bullets,
    ):
        """Respond to keypresses."""
        if event.key == pygame.K_LEFT:
            ship.moving_left = True

        elif event.key == pygame.K_RIGHT:
            ship.moving_right = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet(screen, settings, ship, bullets)

        elif event.key == pygame.K_p:
            if not stats.game_active:
                gf.start_game(screen, settings, stats, sb, ship, aliens, bullets)

        elif event.key == pygame.K_q:
            gf.store_high_score(stats.high_score)
            sys.exit()

    def _check_keyup_events(self, event, ship):
        """Respond to key releases."""
        if event.key == pygame.K_LEFT:
            ship.moving_left = False

        elif event.key == pygame.K_RIGHT:
            ship.moving_right = False

    def _fire_bullet(self, screen, settings, ship, bullets):
        """Create a new bullet and add it to the bullets group."""
        if len(bullets) < settings.bullets_allowed:
            new_bullet = Bullet(screen, settings, ship)
            bullets.add(new_bullet)

    def _update_bullets(self, screen, settings, stats, sb, ship, aliens, bullets):
        """Redraw bullets."""
        bullets.update()

        # Delete off-screen bullets.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        gf.check_bullet_alien_collisions(
            screen,
            settings,
            stats,
            sb,
            ship,
            aliens,
            bullets,
        )


if __name__ == "__main__":
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
