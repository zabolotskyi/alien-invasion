from random import random

import pygame

from alien_invasion import AlienInvasion


class AIPlayer:
    """A bot that plays Alien Invasion."""

    def __init__(self, ai_game):
        self.ai_game = ai_game

    def run_game(self):
        # Run the bot.
        self.ai_game.stats.game_active = True

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Speed up the game for development work.
        self._modify_speed(1)

        # Get the full fleet size.
        self.fleet_size = len(self.ai_game.aliens)

        # Start the main loop for the game.
        while True:
            self.ai_game._check_events()
            self._implement_strategy()

            if self.ai_game.stats.game_active:
                self.ai_game.ship.update()
                self.ai_game._update_bullets()
                self.ai_game._update_aliens()

            self.ai_game._update_screen()

    def _implement_strategy(self):
        # Start chasing aliens if there are no more than a half of them.
        if len(self.ai_game.aliens) <= self.fleet_size / 2:
            self.chase_alien()
        else:
            self._sweep_right_left()

        # Fire bullets at the given frequency, whenever possible.
        self._fire_bullet(0.01)

    def _get_target_alien(self):
        # Find an alien to chase.
        target_alien = self.ai_game.aliens.sprites()[0]

        for alien in self.ai_game.aliens.sprites():
            if alien.rect.y > target_alien.rect.y:
                target_alien = alien
            elif alien.rect.y < target_alien.rect.y:
                continue
            elif alien.rect.x > target_alien.rect.x:
                target_alien = alien

        return target_alien

    def _sweep_right_left(self):
        # Move the ship.
        ship = self.ai_game.ship
        screen_rect = self.ai_game.screen.get_rect()

        if not ship.moving_right and not ship.moving_left:
            ship.moving_right = True
        elif ship.moving_right and ship.rect.right + 10 > screen_rect.right:
            ship.moving_right = False
            ship.moving_left = True
        elif ship.moving_left and ship.rect.left < 10:
            ship.moving_left = False
            ship.moving_right = True

    def _modify_speed(self, speed_factor):
        # Speed up the game if necessary.
        self.ai_game.settings.ship_speed_factor *= speed_factor
        self.ai_game.settings.bullet_speed_factor *= speed_factor
        self.ai_game.settings.alien_speed_factor *= speed_factor

    def _fire_bullet(self, firing_frequency):
        # Fire a bullet with given frequency.
        random_num = random()
        if random_num <= firing_frequency:
            self.ai_game._fire_bullet()

    def chase_alien(self):
        # Get specific alien to chase.
        target_alien = self._get_target_alien()
        ship = self.ai_game.ship

        # Move toward target alien.
        if ship.rect.x < target_alien.rect.x:
            self.ai_game.ship.moving_right = True
            self.ai_game.ship.moving_left = False
        elif ship.rect.x > target_alien.rect.x:
            self.ai_game.ship.moving_right = False
            self.ai_game.ship.moving_left = True


if __name__ == "__main__":
    ai_game = AlienInvasion()

    ai_player = AIPlayer(ai_game)
    ai_player.run_game()
