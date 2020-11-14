"""Utils for handling game process."""
import sys
import pygame

from bullet import Bullet


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


def update_screen(settings, screen, ship, bullets):
    """Handle screen redraws."""
    # Redraw the screen.
    screen.fill(settings.bg_color)
    ship.blitme()

    # Redraw all bullets behind the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(screen, bullets):
    """Redraw bullets."""
    bullets.update()

    # Delete off-screen bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
