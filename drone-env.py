import pygame
import math

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

INITIAL_BOOSTER_ANGLE = 0
ANGLE_RANGE = 45
INITIAL_FIRE_ON = False
BOOSTER_ANGLE_INCREMENT = 0.3

THRUST = 0.0055
GRAVITY = 0.008
THRUST_X_COMPONENT = 0.8
THRUST_Y_COMPONENT = 1

DIMENSION_MULTIPLIER = 8

# Initialize the game
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LunAIr")
icon = pygame.image.load('imgs/rocket.png')
pygame.display.set_icon(icon)

# Load images
rocket_img = pygame.image.load('imgs/body.png')
rocket_img = pygame.transform.scale(rocket_img, (5 * DIMENSION_MULTIPLIER, 10 * DIMENSION_MULTIPLIER))
booster_img = pygame.image.load('imgs/booster.png')
booster_img = pygame.transform.scale(booster_img, (2 * DIMENSION_MULTIPLIER, 4 * DIMENSION_MULTIPLIER))
fire_img = pygame.image.load('imgs/fire.png')
fire_img = pygame.transform.scale(fire_img, (2 *DIMENSION_MULTIPLIER, 4 * DIMENSION_MULTIPLIER))

def draw_booster(x, y, angle, fire_on):
    """Draw booster with optional fire."""
    # Rotate the booster
    rotated_booster = pygame.transform.rotate(booster_img, angle)
    booster_rect = rotated_booster.get_rect(center=(x, y))

    if fire_on:
        # Calculate the position of the fire
        fire_offset = 1.8 * DIMENSION_MULTIPLIER + booster_img.get_height() // 2
        fire_x = x + fire_offset * math.sin(math.radians(angle))
        fire_y = y + fire_offset * math.cos(math.radians(angle))

        # Rotate and draw the fire
        rotated_fire = pygame.transform.rotate(fire_img, angle)
        fire_rect = rotated_fire.get_rect(center=(fire_x, fire_y))
        screen.blit(rotated_fire, fire_rect.topleft)

    screen.blit(rotated_booster, booster_rect.topleft)

def draw_rocket(x, y, angle1, angle2, fire1_on, fire2_on):
    """Draw rocket with two boosters."""

    screen.blit(rocket_img, (x, y))

    # Draw boosters
    draw_booster(x + 6.5 * DIMENSION_MULTIPLIER, y + 8.5 * DIMENSION_MULTIPLIER, angle1, fire1_on)
    draw_booster(x - 1.5 * DIMENSION_MULTIPLIER, y + 8.5 * DIMENSION_MULTIPLIER, angle2, fire2_on)



def clamp_angle(angle):
    """Clamp angle to be within the range -ANGLE_RANGE to +ANGLE_RANGE."""
    return max(-ANGLE_RANGE, min(ANGLE_RANGE, angle))

# Main game loop
running = True
booster_angle_1 = INITIAL_BOOSTER_ANGLE
booster_angle_2 = INITIAL_BOOSTER_ANGLE
fire_1_on = INITIAL_FIRE_ON
fire_2_on = INITIAL_FIRE_ON

rocket_x = SCREEN_WIDTH // 2
rocket_y = SCREEN_HEIGHT // 2
velocity_x = 0
velocity_y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            fire_1_on = False
            fire_2_on = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        booster_angle_1 = clamp_angle(booster_angle_1 + BOOSTER_ANGLE_INCREMENT)
        fire_1_on = True
    if keys[pygame.K_RIGHT]:
        booster_angle_1 = clamp_angle(booster_angle_1 - BOOSTER_ANGLE_INCREMENT)
        fire_1_on = True
    if keys[pygame.K_a]:
        booster_angle_2 = clamp_angle(booster_angle_2 + BOOSTER_ANGLE_INCREMENT)
        fire_2_on = True
    if keys[pygame.K_d]:
        booster_angle_2 = clamp_angle(booster_angle_2 - BOOSTER_ANGLE_INCREMENT)
        fire_2_on = True
    
    if keys[pygame.K_t]:
        fire_1_on = True
        fire_2_on = True


    # Apply gravity
    velocity_y += GRAVITY

    # Apply thrust
    if fire_1_on:
        velocity_x -= 0.8 * THRUST * math.sin(math.radians(booster_angle_1))
        velocity_y -= THRUST * math.cos(math.radians(booster_angle_1))
    if fire_2_on:
        velocity_x -= 0.8 * THRUST * math.sin(math.radians(booster_angle_2))
        velocity_y -= THRUST * math.cos(math.radians(booster_angle_2))

    # Update rocket position
    rocket_x += velocity_x
    rocket_y += velocity_y

    # Clamp rocket position to screen bounds and reset velocity if hitting bounds
    if rocket_x < 0:
        rocket_x = 0
        velocity_x = 0
    elif rocket_x > SCREEN_WIDTH - rocket_img.get_width():
        rocket_x = SCREEN_WIDTH - rocket_img.get_width()
        velocity_x = 0
    
    if rocket_y < 0:
        rocket_y = 0
        velocity_y = 0
    elif rocket_y > SCREEN_HEIGHT - rocket_img.get_height():
        rocket_y = SCREEN_HEIGHT - rocket_img.get_height()
        velocity_y = 0

    # Clear screen
    screen.fill((0, 0, 0))
    
    # Draw rocket
    draw_rocket(rocket_x, rocket_y, booster_angle_1, booster_angle_2, fire_1_on, fire_2_on)
    
    pygame.display.update()

pygame.quit()
