"""Alien Invasion game."""
import sys
import json
from time import sleep

import pygame
from pygame.sprite import Group

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship

from consts import game_stats_file


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
        self.play_button = Button(self, "Play")

        # Create an instance of game stats.
        self.stats = GameStats(self)

        # Make a scoreboard.
        self.sb = Scoreboard(self)

        # Make a ship.
        self.ship = Ship(self)

        # Make a group of bullets.
        self.bullets = Group()

        # Make a group of aliens.
        self.aliens = Group()

        # Create the fleet of aliens.
        self._create_fleet()

    def run_game(self):
        # Start the main loop for the game.
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._store_high_score()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self._check_play_button(mouse_x, mouse_y)

    def _update_screen(self):
        """Handle screen redraws."""
        # Redraw the screen.
        self.screen.fill(self.settings.bg_color)

        # Redraw all bullets behind the ship and aliens.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw scores.
        self.sb.show_score()

        # Draw a play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

        elif event.key == pygame.K_q:
            self._store_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Redraw bullets."""
        self.bullets.update()

        # Delete off-screen bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _create_fleet(self):
        """Create a full fleet of aliens."""
        # Create an alien and find the number of aliens in the row.
        # The distance between aliens is one alien width.
        alien = Alien(self)
        number_aliens_x = self._get_number_columns(alien.rect.width)
        number_aliens_y = self._get_number_rows(alien.rect.height)

        # Create the fleet of aliens.
        for row_number in range(number_aliens_y):
            for column_number in range(number_aliens_x):
                self._create_alien(column_number, row_number)

    def _start_game(self):
        # Reset dynamic game settings.
        self.settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset game stats.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Reset the scoreboard and ships images.
        self.sb.prep_images()

        # Clean the screen from aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Center the ship and refill the aliens.
        self.ship.center_ship()
        self._create_fleet()

    def _start_new_level(self):
        # Destroy all bullets, increase the game tempo and refill the aliens.
        self.bullets.empty()
        self.settings.increase_speed()
        self._create_fleet()

        # Increase the level.
        self.stats.level += 1
        self.sb.prep_level()

    def _ship_hit(self):
        """Respond to alien-ship collision."""
        if self.stats.ships_left > 1:
            # Decrement ship count.
            self.stats.ships_left -= 1

            # Update scoreboard.
            self.sb.prep_ships()

            # Clean the screen from aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Center the ship and refill the aliens.
            self.ship.center_ship()
            self._create_fleet()

            # Leave the player some time to relax.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_play_button(self, mouse_x, mouse_y):
        """Start a new game if Play is pressed."""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)

        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check whether there is any collision between a bullet and an alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += len(aliens) * self.settings.alien_points
                self.sb.prep_score()
                self.sb.prep_high_score()

            self._check_high_score()

        if len(self.aliens) == 0:
            self._start_new_level()

    def _check_aliens_bottom(self):
        """Check if any alien has reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.height:
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for alien-bottom collisions.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any alien has reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the fleet and reverse the direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _check_high_score(self):
        # Update the high score.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def _get_number_columns(self, alien_width):
        """Calculate the amount of aliens that fit into one row."""
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def _get_number_rows(self, alien_height):
        """Calculate the amount of alien rows."""
        available_space_y = self.settings.screen_height - (
            3 * alien_height + self.ship.rect.height
        )
        number_aliens_y = int(available_space_y / (2 * alien_height))
        return number_aliens_y

    def _create_alien(self, alien_number_x, alien_number_y):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + (2 * alien_number_x * alien_width)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2 * alien_number_y * alien_height)
        self.aliens.add(alien)

    def _store_high_score(self):
        with open(game_stats_file, "w") as file:
            json.dump(self.stats.high_score, file)


if __name__ == "__main__":
    # Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
