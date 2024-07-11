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
DRONE_WIDTH = float(config['DEFAULT']['DRONE_BODY_WIDTH'])
DRONE_HEIGHT = float(config['DEFAULT']['DRONE_BODY_HEIGHT'])
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
pygame.display.set_caption("roc-swarm")
icon = pygame.image.load('res/rocket.png')
pygame.display.set_icon(icon)

# Load images
drone_body_img = pygame.image.load('res/body.png')
drone_body_img = pygame.transform.scale(drone_body_img, (int(DRONE_WIDTH * DIMENSION_MULTIPLIER), int(DRONE_HEIGHT * DIMENSION_MULTIPLIER)))
booster_img = pygame.image.load('res/booster.png')
booster_img = pygame.transform.scale(booster_img, (int(BOOSTER_WIDTH * DIMENSION_MULTIPLIER), int(BOOSTER_HEIGHT * DIMENSION_MULTIPLIER)))
fire_img = pygame.image.load('res/fire.png')
fire_img = pygame.transform.scale(fire_img, (int(FIRE_WIDTH * DIMENSION_MULTIPLIER), int(FIRE_HEIGHT * DIMENSION_MULTIPLIER)))
target_img = pygame.image.load('res/target.png')
target_img = pygame.transform.scale(target_img, (int(TARGET_SIDE * DIMENSION_MULTIPLIER), int(TARGET_SIDE * DIMENSION_MULTIPLIER)))

class Booster:
    def __init__(self, x, y, isBooster2=False):
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
        self.booster_rect = booster_img.get_rect(center=(self.x, self.y))
        self.isBooster2 = isBooster2

        # Drone body setup
        self.drone_body_img = drone_body_img
        self.drone_body_rect = self.drone_body_img.get_rect(center=(self.x, self.y))

    def draw_direction_arrow(self, other_booster):
        # Calculate center positions
        self_center_x, self_center_y = self.booster_rect.center
        other_center_x, other_center_y = other_booster.booster_rect.center

        # Midpoint between the two centers
        midpoint_x = (self_center_x + other_center_x) / 2
        midpoint_y = (self_center_y + other_center_y) / 2

        # Vector from self to other booster
        dx = other_center_x - self_center_x
        dy = other_center_y - self_center_y

        # Calculate perpendicular direction
        length = math.sqrt(dx ** 2 + dy ** 2)
        if length > 0:
            perp_dx = -dy / length  # Perpendicular x direction
            perp_dy = dx / length   # Perpendicular y direction

            # Calculate arrow position
            arrow_length = 20
            arrow_end_x = midpoint_x + perp_dx * arrow_length
            arrow_end_y = midpoint_y + perp_dy * arrow_length

            # Draw arrow
            pygame.draw.line(screen, (255, 0, 0), (midpoint_x, midpoint_y), (arrow_end_x, arrow_end_y), 3)
    
    def get_tilt(self, other_booster):
        return math.degrees(math.atan2(other_booster.y - self.y, other_booster.x - self.x))
    
    def draw(self):

        # Draw the booster and fire
        self.draw_booster(self.x + BOOSTER_WIDTH // 2  * DIMENSION_MULTIPLIER, self.y + 5.5 * DIMENSION_MULTIPLIER, self.booster_angle_1, self.fire_1_on)

        # Draw the direction arrow
        if not self.isBooster2:
            self.draw_direction_arrow(drone.booster_2)
        else:
            self.draw_direction_arrow(drone.booster_1)

    def draw_booster(self, x, y, angle, fire_on):
        rotated_booster = pygame.transform.rotate(booster_img, angle)
        booster_rect = rotated_booster.get_rect(center=(x, y))

        if fire_on:
            fire_offset = 3.5 * DIMENSION_MULTIPLIER + booster_img.get_height() // 2
            fire_x = x + fire_offset * math.sin(math.radians(angle))
            fire_y = y + fire_offset * math.cos(math.radians(angle))

            rotated_fire = pygame.transform.rotate(fire_img, angle)
            fire_rect = rotated_fire.get_rect(center=(fire_x, fire_y))
            screen.blit(rotated_fire, fire_rect.topleft)

        screen.blit(rotated_booster, booster_rect.topleft)

    def clamp_angle(self, angle):
        return max(-ANGLE_RANGE, min(ANGLE_RANGE, angle))

    def update(self):
        keys = pygame.key.get_pressed()

        # if any key is unpressed, turn off the fire
        self.fire_1_on = False
        self.fire_2_on = False

        if not self.isBooster2:
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

        self.booster_rect.x = self.x
        self.booster_rect.y = self.y
        self.drone_body_rect.x = self.x
        self.drone_body_rect.y = self.y

        # Prevent drone from moving out of the screen and stop velocity on collision
        if self.x < 0:
            self.x = 0
            self.velocity_x = 0
        elif self.x > SCREEN_WIDTH - booster_img.get_width():
            self.x = SCREEN_WIDTH - booster_img.get_width()
            self.velocity_x = 0

        if self.y < 0:
            self.y = 0
            self.velocity_y = 0
        elif self.y > SCREEN_HEIGHT - booster_img.get_height():
            self.y = SCREEN_HEIGHT - booster_img.get_height()
            self.velocity_y = 0

        # Check for collision with the current target
        if self.current_target_index < len(TARGETS):
            target_x, target_y = TARGETS[self.current_target_index]
            target_center_x = target_x + TARGET_SIDE * DIMENSION_MULTIPLIER / 2
            target_center_y = target_y + TARGET_SIDE * DIMENSION_MULTIPLIER / 2

            # Calculate distance between drone tip and target center
            distance = math.sqrt((self.x + booster_img.get_width() / 2 - target_center_x) ** 2 +
                                (self.y - target_center_y) ** 2)

            # Score inversely proportional to distance
            if distance > 0:
                self.score += 100 / distance

    def adjust_position(self, other_drone):
        # Maintain constant distance between drones
        distance = math.sqrt((self.x - other_drone.x) ** 2 + (self.y - other_drone.y) ** 2)
        if distance != 0:
            scale = 100 / distance
            self.x = other_drone.x + (self.x - other_drone.x) * scale
            self.y = other_drone.y + (self.y - other_drone.y) * scale
            self.booster_rect.x = self.x
            self.booster_rect.y = self.y
            self.drone_body_rect.x = self.x
            self.drone_body_rect.y = self.y

    def draw_target(self):
        if self.current_target_index < len(TARGETS):
            target_x, target_y = TARGETS[self.current_target_index]
            target_rect = target_img.get_rect(center=(target_x, target_y))
            screen.blit(target_img, target_rect.topleft)

class Drone:
    def __init__(self, x1, y1, x2, y2):
        self.booster_1 = Booster(x1, y1)
        self.booster_2 = Booster(x2, y2, isBooster2=True)

    def update(self):
        self.booster_1.update()
        self.booster_2.update()
        self.booster_1.adjust_position(self.booster_2)
        self.booster_2.adjust_position(self.booster_1)

    def draw(self):
        self.booster_1.draw()
        self.booster_2.draw()
        self.booster_1.draw_target()
        self.booster_2.draw_target()

    def get_score(self):
        return self.booster_1.score + self.booster_2.score

# Create instances of drone
drone = Drone(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 2)  # Example positions

# Main game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    drone.update()

    screen.fill((0, 0, 0))
    drone.draw()

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {drone.get_score():.2f}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display tilt of the rod
    font = pygame.font.SysFont(None, 36)
    tilt_text = font.render(f'Tilt: {drone.booster_1.get_tilt(drone.booster_2):.2f}', True, (255, 255, 255))
    screen.blit(tilt_text, (10, 40))


    # Check if game duration has passed
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= GAME_DURATION:
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
