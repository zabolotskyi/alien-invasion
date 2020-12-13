"""Utils for handling game process."""
import json
import pygame
from time import sleep

from alien import Alien
from consts import game_stats_file


def store_high_score(high_score):
    with open(game_stats_file, "w") as file:
        json.dump(high_score, file)


def start_game(screen, settings, stats, sb, ship, aliens, bullets):
    # Reset dynamic game settings.
    settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset game stats.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard and ships images.
    sb.prep_images()

    # Clean the screen from aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Center the ship and refill the aliens.
    ship.center_ship()
    create_fleet(screen, settings, ship, aliens)


def check_play_button(
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
):
    """Start a new game if Play is pressed."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        start_game(screen, settings, stats, sb, ship, aliens, bullets)


def start_new_level(screen, settings, stats, sb, ship, aliens, bullets):
    # Destroy all bullets, increase the game tempo and refill the aliens.
    bullets.empty()
    settings.increase_speed()
    create_fleet(screen, settings, ship, aliens)

    # Increase the level.
    stats.level += 1
    sb.prep_level()


def check_bullet_alien_collisions(
    screen,
    settings,
    stats,
    sb,
    ship,
    aliens,
    bullets,
):
    """Respond to bullet-alien collisions."""
    # Check whether there is any collision between a bullet and an alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += len(aliens) * settings.alien_points
            sb.prep_score()
            sb.prep_high_score()

        check_high_score(stats, sb)

    if len(aliens) == 0:
        start_new_level(screen, settings, stats, sb, ship, aliens, bullets)


def get_number_columns(settings, alien_width):
    """Calculate the amount of aliens that fit into one row."""
    available_space_x = settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(settings, alien_height, ship_height):
    """Calculate the amount of alien rows."""
    available_space_y = settings.screen_height - (3 * alien_height + ship_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def create_alien(screen, settings, aliens, alien_number_x, alien_number_y):
    """Create an alien and place it in the row."""
    alien = Alien(screen, settings)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + (2 * alien_number_x * alien_width)
    alien.rect.x = alien.x
    alien.rect.y = alien_height + (2 * alien_number_y * alien_height)
    aliens.add(alien)


def create_fleet(screen, settings, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in the row.
    # The distance between aliens is one alien width.
    alien = Alien(screen, settings)
    number_aliens_x = get_number_columns(settings, alien.rect.width)
    number_aliens_y = get_number_rows(
        settings,
        alien.rect.height,
        ship.rect.height,
    )

    # Create the fleet of aliens.
    for row_number in range(number_aliens_y):
        for column_number in range(number_aliens_x):
            create_alien(screen, settings, aliens, column_number, row_number)


def check_fleet_edges(settings, aliens):
    """Respond appropriately if any alien has reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    """Drop the fleet and reverse the direction."""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed

    settings.fleet_direction *= -1


def check_high_score(stats, sb):
    # Update the high score.
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def ship_hit(screen, settings, stats, sb, ship, aliens, bullets):
    """Respond to alien-ship collision."""
    if stats.ships_left > 1:
        # Decrement ship count.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Clean the screen from aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Center the ship and refill the aliens.
        ship.center_ship()
        create_fleet(screen, settings, ship, aliens)

        # Leave the player some time to relax.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, settings, stats, sb, ship, aliens, bullets):
    """Check if any alien has reached the bottom of the screen."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.height:
            ship_hit(screen, settings, stats, sb, ship, aliens, bullets)
            break


def update_aliens(screen, settings, stats, sb, ship, aliens, bullets):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(screen, settings, stats, sb, ship, aliens, bullets)

    # Look for alien-bottom collisions.
    check_aliens_bottom(screen, settings, stats, sb, ship, aliens, bullets)
