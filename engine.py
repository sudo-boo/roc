import math
import pygame
import configparser

# Constants (assuming these are loaded from config.ini as before)
config = configparser.ConfigParser()
config.read('config.ini')
SCREEN_WIDTH = int(config['DEFAULT']['SCREEN_WIDTH'])
SCREEN_HEIGHT = int(config['DEFAULT']['SCREEN_HEIGHT'])
DIMENSION_MULTIPLIER = float(config['DEFAULT']['DIMENSION_MULTIPLIER'])
ANGLE_RANGE = float(config['DEFAULT']['ANGLE_RANGE'])
INITIAL_BOOSTER_ANGLE_1 = float(config['DEFAULT']['INITIAL_BOOSTER_ANGLE_1'])
INITIAL_BOOSTER_ANGLE_2 = float(config['DEFAULT']['INITIAL_BOOSTER_ANGLE_2'])
BOOSTER_ANGLE_INCREMENT = float(config['DEFAULT']['BOOSTER_ANGLE_INCREMENT'])
INITIAL_FIRE_ON = config.getboolean('DEFAULT', 'INITIAL_FIRE_ON')
THRUST = float(config['DEFAULT']['THRUST'])
GRAVITY = float(config['DEFAULT']['GRAVITY'])
THRUST_X_COMPONENT = float(config['DEFAULT']['THRUST_X_COMPONENT'])
THRUST_Y_COMPONENT = float(config['DEFAULT']['THRUST_Y_COMPONENT'])
ROCKET_HEIGHT = float(config['DEFAULT']['ROCKET_BODY_HEIGHT'])
ROCKET_WIDTH = float(config['DEFAULT']['ROCKET_BODY_WIDTH'])
BOOSTER_HEIGHT = float(config['DEFAULT']['BOOSTER_HEIGHT'])
BOOSTER_WIDTH = float(config['DEFAULT']['BOOSTER_WIDTH'])
FIRE_HEIGHT = float(config['DEFAULT']['FIRE_HEIGHT'])
FIRE_WIDTH = float(config['DEFAULT']['FIRE_WIDTH'])
TARGET_SIDE = float(config['DEFAULT']['TARGET_SIDE'])
GAME_DURATION = int(config['DEFAULT']['GAME_DURATION']) * 1000
TARGETS = [(0, 0), (450, 200), (600, 600)]  # Assuming TARGETS is also read from config

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Game")
icon = pygame.image.load('res/rocket.png')
pygame.display.set_icon(icon)

# Load images
rocket_img = pygame.image.load('res/body.png')
rocket_img = pygame.transform.scale(rocket_img, (int(ROCKET_WIDTH * DIMENSION_MULTIPLIER), int(ROCKET_HEIGHT * DIMENSION_MULTIPLIER)))
booster_img = pygame.image.load('res/booster.png')
booster_img = pygame.transform.scale(booster_img, (int(BOOSTER_WIDTH * DIMENSION_MULTIPLIER), int(BOOSTER_HEIGHT * DIMENSION_MULTIPLIER)))
fire_img = pygame.image.load('res/fire.png')
fire_img = pygame.transform.scale(fire_img, (int(FIRE_WIDTH * DIMENSION_MULTIPLIER), int(FIRE_HEIGHT * DIMENSION_MULTIPLIER)))
target_img = pygame.image.load('res/target.png')
target_img = pygame.transform.scale(target_img, (int(TARGET_SIDE * DIMENSION_MULTIPLIER), int(TARGET_SIDE * DIMENSION_MULTIPLIER)))

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.booster_angle_1 = INITIAL_BOOSTER_ANGLE_1
        self.booster_angle_2 = INITIAL_BOOSTER_ANGLE_2
        self.fire_1_on = INITIAL_FIRE_ON
        self.fire_2_on = INITIAL_FIRE_ON
        self.velocity_x = 0
        self.velocity_y = 0
        self.score = 0
        self.current_target_index = 0
        self.rocket_rect = rocket_img.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(rocket_img, self.rocket_rect.topleft)
        self.draw_booster(self.x + 6.5 * DIMENSION_MULTIPLIER, self.y + 8.5 * DIMENSION_MULTIPLIER, self.booster_angle_1, self.fire_1_on)
        self.draw_booster(self.x - 1.5 * DIMENSION_MULTIPLIER, self.y + 8.5 * DIMENSION_MULTIPLIER, self.booster_angle_2, self.fire_2_on)

    def draw_booster(self, x, y, angle, fire_on):
        rotated_booster = pygame.transform.rotate(booster_img, angle)
        booster_rect = rotated_booster.get_rect(center=(x, y))

        if fire_on:
            fire_offset = 1.8 * DIMENSION_MULTIPLIER + booster_img.get_height() // 2
            fire_x = x + fire_offset * math.sin(math.radians(angle))
            fire_y = y + fire_offset * math.cos(math.radians(angle))

            rotated_fire = pygame.transform.rotate(fire_img, angle)
            fire_rect = rotated_fire.get_rect(center=(fire_x, fire_y))
            screen.blit(rotated_fire, fire_rect.topleft)

        screen.blit(rotated_booster, booster_rect.topleft)

    def clamp_angle(self, angle):
        return max(-ANGLE_RANGE, min(ANGLE_RANGE, angle))

    def update(self, isRocket2=False):
        keys = pygame.key.get_pressed()

        # if any key is unpressed, turn off the fire
        self.fire_1_on = False
        self.fire_2_on = False

        if not isRocket2:
            if keys[pygame.K_LEFT]:
                self.booster_angle_1 = self.clamp_angle(self.booster_angle_1 + BOOSTER_ANGLE_INCREMENT)
                self.booster_angle_2 = self.clamp_angle(self.booster_angle_2 + BOOSTER_ANGLE_INCREMENT)
                self.fire_1_on = True
                self.fire_2_on = True
            if keys[pygame.K_RIGHT]:
                self.booster_angle_1 = self.clamp_angle(self.booster_angle_1 - BOOSTER_ANGLE_INCREMENT)
                self.booster_angle_2 = self.clamp_angle(self.booster_angle_2 - BOOSTER_ANGLE_INCREMENT)
                self.fire_1_on = True
                self.fire_2_on = True
        else:
            if keys[pygame.K_a]:
                self.booster_angle_1 = self.clamp_angle(self.booster_angle_1 + BOOSTER_ANGLE_INCREMENT)
                self.booster_angle_2 = self.clamp_angle(self.booster_angle_2 + BOOSTER_ANGLE_INCREMENT)
                self.fire_1_on = True
                self.fire_2_on = True
            if keys[pygame.K_d]:
                self.booster_angle_1 = self.clamp_angle(self.booster_angle_1 - BOOSTER_ANGLE_INCREMENT)
                self.booster_angle_2 = self.clamp_angle(self.booster_angle_2 - BOOSTER_ANGLE_INCREMENT)
                self.fire_1_on = True
                self.fire_2_on = True

        if keys[pygame.K_t]:
            self.fire_1_on = True
            self.fire_2_on = True

        self.velocity_y += GRAVITY

        if self.fire_1_on:
            self.velocity_x -= 0.8 * THRUST * math.sin(math.radians(self.booster_angle_1))
            self.velocity_y -= THRUST * math.cos(math.radians(self.booster_angle_1))
        if self.fire_2_on:
            self.velocity_x -= 0.8 * THRUST * math.sin(math.radians(self.booster_angle_2))
            self.velocity_y -= THRUST * math.cos(math.radians(self.booster_angle_2))

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.rocket_rect.x = self.x
        self.rocket_rect.y = self.y

        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x > SCREEN_WIDTH - rocket_img.get_width():
            self.x = SCREEN_WIDTH - rocket_img.get_width()
            self.velocity_x = 0

        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        elif self.y > SCREEN_HEIGHT - rocket_img.get_height():
            self.y = SCREEN_HEIGHT - rocket_img.get_height()
            self.velocity_y = 0

        # Keep constant distance between rockets
        if not isRocket2:
            rocket2.adjust_position(self)
        else:
            self.adjust_position(rocket2)

        # Check for collision with the current target
        if self.current_target_index < len(TARGETS):
            target_x, target_y = TARGETS[self.current_target_index]
            target_center_x = target_x + TARGET_SIDE * DIMENSION_MULTIPLIER / 2
            target_center_y = target_y + TARGET_SIDE * DIMENSION_MULTIPLIER / 2

            # Calculate distance between rocket tip and target center
            distance = math.sqrt((self.x + rocket_img.get_width() / 2 - target_center_x) ** 2 +
                                 (self.y - target_center_y) ** 2)

            # Score inversely proportional to distance
            if distance > 0:
                self.score += 100 / distance

    def adjust_position(self, other_rocket):
        # Maintain constant distance between rockets
        distance = math.sqrt((self.x - other_rocket.x) ** 2 + (self.y - other_rocket.y) ** 2)
        if distance != 0:
            scale = 100 / distance
            self.x = other_rocket.x + (self.x - other_rocket.x) * scale
            self.y = other_rocket.y + (self.y - other_rocket.y) * scale
            self.rocket_rect.x = self.x
            self.rocket_rect.y = self.y

    def draw_target(self):
        if self.current_target_index < len(TARGETS):
            target_x, target_y = TARGETS[self.current_target_index]
            target_rect = target_img.get_rect(center=(target_x, target_y))
            screen.blit(target_img, target_rect.topleft)

    def draw_connecting_rod(self, other_rocket):
        # Calculate positions of rockets
        rocket1_center = (self.x + rocket_img.get_width() // 2, self.y + rocket_img.get_height() // 2)
        rocket2_center = (other_rocket.x + rocket_img.get_width() // 2, other_rocket.y + rocket_img.get_height() // 2)

        # Calculate distance and direction vector
        distance = math.sqrt((rocket1_center[0] - rocket2_center[0]) ** 2 + (rocket1_center[1] - rocket2_center[1]) ** 2)
        direction = ((rocket2_center[0] - rocket1_center[0]), (rocket2_center[1] - rocket1_center[1]))

        # Normalize direction vector
        if distance > 0:
            direction = (direction[0] / distance, direction[1] / distance)

        # Calculate rod end positions
        rod_length = 100
        rod_end1 = (rocket1_center[0] + direction[0] * rod_length, rocket1_center[1] + direction[1] * rod_length)
        rod_end2 = (rocket2_center[0] - direction[0] * rod_length, rocket2_center[1] - direction[1] * rod_length)

        # Draw the rod
        pygame.draw.line(screen, (255, 255, 255), rod_end1, rod_end2, 3)

# Create instances of Rocket
rocket = Rocket(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2)  # Example position for the first rocket
rocket2 = Rocket(SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 2)  # Example position for the second rocket

# Main game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rocket.update()
    rocket2.update(isRocket2=True)

    screen.fill((0, 0, 0))
    rocket.draw()
    rocket2.draw()
    rocket.adjust_position(rocket2)
    rocket2.adjust_position(rocket)
    rocket.draw_target()
    rocket2.draw_target()

    # Draw connecting rod between rockets
    rocket.draw_connecting_rod(rocket2)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {rocket.score:.2f}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Check if 20 seconds have passed
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= GAME_DURATION:
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
