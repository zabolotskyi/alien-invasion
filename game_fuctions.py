"""Utils for handling game process."""
import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def fire_bullet(settings, screen, ship, bullets):
    """Create a new bullet and add it to the bullets group."""
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

    elif event.key == pygame.K_RIGHT:
        ship.moving_right = False


def check_events(settings, screen, ship, bullets):
    """Respond to keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(settings, screen, ship, aliens, bullets):
    """Handle screen redraws."""
    # Redraw the screen.
    screen.fill(settings.bg_color)

    # Redraw all bullets behind the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_bullet_alien_collisions(screen, settings, aliens, ship, bullets):
    """Respond to bullet-alien collisions."""
    # Check whether there is any collision between a bullet and an alien.
    pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy all bullets and refill the aliens.
        bullets.empty()
        create_fleet(screen, settings, aliens, ship)


def update_bullets(screen, settings, aliens, ship, bullets):
    """Redraw bullets."""
    bullets.update()

    # Delete off-screen bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(screen, settings, aliens, ship, bullets)


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


def create_fleet(screen, settings, aliens, ship):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in the row.
    # The distance between aliens is one alien width.
    alien = Alien(screen, settings)
    number_aliens_x = get_number_columns(settings, alien.rect.width)
    number_aliens_y = get_number_rows(settings, alien.rect.height, ship.rect.height)

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


def ship_hit(screen, settings, ship, aliens, bullets, stats):
    """Respond to alien-ship collision."""
    if stats.ships_left > 0:
        # Decrement ship count.
        stats.ships_left -= 1

        # Clean the screen from aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Center the ship and refill the aliens.
        ship.center_ship()
        create_fleet(screen, settings, aliens, ship)

        # Leave the player some time to relax.
        sleep(0.5)

    else:
        stats.game_active = False


def check_aliens_bottom(screen, settings, ship, aliens, bullets, stats):
    """Check if any alien has reached the bottom of the screen."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.height:
            ship_hit(screen, settings, ship, aliens, bullets, stats)
            break


def update_aliens(screen, settings, ship, aliens, bullets, stats):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(screen, settings, ship, aliens, bullets, stats)

    # Look for alien-bottom collisions.
    check_aliens_bottom(screen, settings, ship, aliens, bullets, stats)
