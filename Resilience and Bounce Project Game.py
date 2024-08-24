import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (0, 0, 0)  # Black background
ENEMY_COLOR = (255, 0, 0)  # Red color
DEFENSE_COLOR = (0, 0, 255)  # Blue color
ENEMY_RADIUS = 15
DEFENSE_HEIGHT = 20
DEFENSE_WIDTH = SCREEN_WIDTH
INITIAL_ENEMY_SPEED = 2
ENEMY_SPEED_INCREMENT = 0.01
DEFENSE_COST = 3
POINT_INTERVAL = 500  # 500 milliseconds for 1 point
LIFE_COST = 5
INITIAL_LIVES = 3
FADE_OUT_DURATION = 60  # Number of frames for the fade out effect
BOUNCE_DISAPPEAR_TIME = 2000  # 2 seconds in milliseconds
BRONZE_MEDAL_TIME = 15000  # 15 seconds in milliseconds
SILVER_MEDAL_TIME = 30000  # 30 seconds in milliseconds
GOLD_MEDAL_TIME = 60000  # 60 seconds in milliseconds

# Load heart image
HEART_IMAGE = pygame.image.load('Video_Game_Heart.png')
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (30, 30))  # Scale the image to fit nicely
HEART_WIDTH = HEART_IMAGE.get_width()
HEART_HEIGHT = HEART_IMAGE.get_height()

# Load medal images
BRONZE_MEDAL_IMAGE = pygame.image.load('bronze_medal.png')
BRONZE_MEDAL_IMAGE = pygame.transform.scale(BRONZE_MEDAL_IMAGE, (50, 65))
SILVER_MEDAL_IMAGE = pygame.image.load('silver_medal.png')
SILVER_MEDAL_IMAGE = pygame.transform.scale(SILVER_MEDAL_IMAGE, (50, 70))
GOLD_MEDAL_IMAGE = pygame.image.load('gold_medal.png')
GOLD_MEDAL_IMAGE = pygame.transform.scale(GOLD_MEDAL_IMAGE, (50, 65))

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BOUNCE")

# Define player properties
player_points = 0
player_lives = INITIAL_LIVES
last_point_time = pygame.time.get_ticks()
enemy_speed = INITIAL_ENEMY_SPEED
start_time = pygame.time.get_ticks()  # Track the start time

# Function to create enemies
def create_enemy():
    x_pos = random.randint(ENEMY_RADIUS, SCREEN_WIDTH - ENEMY_RADIUS)
    y_pos = 0
    return [x_pos, y_pos, enemy_speed, ENEMY_COLOR, 255, None]  # Add a field for bounce time

# List to hold all enemies and defenses
enemies = [create_enemy()]
defenses = []

# Function to detect collisions
def detect_collision(enemy, defense_y, enemy_radius, defense_height):
    e_x, e_y, *_ = enemy
    if defense_y <= e_y <= defense_y + defense_height:
        return True
    return False

# Function to display text
def draw_text(surface, text, font, color, pos):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=pos)
    surface.blit(text_obj, text_rect)

# Function to draw hearts for lives
def draw_hearts(surface, x, y, lives):
    for i in range(lives):
        surface.blit(HEART_IMAGE, (x + i * (HEART_WIDTH + 5), y))

# Function to draw the main menu
def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont("monospace", 60)
    draw_text(screen, "BOUNCE", font, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    draw_text(screen, "Click to Start", font, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    instructions_font = pygame.font.SysFont("monospace", 30)
    instructions = [
        "Instructions:",
        "1. Click to place a horizontal defense.",
        "2. Defenses cost 3 points each.",
        "3. Defenses disappear after blocking 3 enemies.",
        "4. Earn 1 point every half second.",
        "5. Lose a life if an enemy reaches the bottom.",
        "6. Click on hearts to buy lives for 5 points each.",
        "7. Enemy speed increases over time.",
        "8. Enemies bounce and fade out when hitting defenses.",
        "9. Game over when lives reach 0."
    ]
    for i, line in enumerate(instructions):
        draw_text(screen, line, instructions_font, (255, 255, 255), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100 + i * 30))
    pygame.display.flip()

# Main game loop
running = True
menu = True
clock = pygame.time.Clock()

while running:
    if menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu = False
                start_time = pygame.time.get_ticks()  # Reset start time when game starts
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if clicking on hearts to buy lives
                heart_x_start = SCREEN_WIDTH - (INITIAL_LIVES + 1) * (HEART_WIDTH + 5)
                if heart_x_start <= mouse_x <= SCREEN_WIDTH and 20 <= mouse_y <= 20 + HEART_HEIGHT:
                    if player_points >= LIFE_COST:
                        player_lives += 1
                        player_points -= LIFE_COST
                else:
                    if player_points >= DEFENSE_COST:
                        # Purchase a defense
                        defenses.append([mouse_y, 0])  # Initialize defense collision count to 0
                        player_points -= DEFENSE_COST

        # Update enemy positions
        current_time = pygame.time.get_ticks()
        for enemy in enemies[:]:
            if enemy[4] > 0:  # If the enemy is not fully faded out
                enemy[1] += enemy[2]
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_lives -= 1
                if player_lives == 0:
                    running = False  # Game over

            for defense in defenses[:]:
                if detect_collision(enemy, defense[0], ENEMY_RADIUS, DEFENSE_HEIGHT):
                    enemy[2] = -enemy[2]  # Bounce back
                    defense[1] += 1  # Increment collision count for defense
                    if defense[1] >= 3:
                        defenses.remove(defense)
                    enemy[4] -= 255 // FADE_OUT_DURATION  # Reduce alpha value
                    if enemy[5] is None:  # If the enemy has just bounced
                        enemy[5] = current_time  # Set the bounce time

            # Check if the enemy should disappears
            if enemy[5] is not None and current_time - enemy[5] >= BOUNCE_DISAPPEAR_TIME:
                enemies.remove(enemy)

        # Increase enemy speed
        enemy_speed += ENEMY_SPEED_INCREMENT

        # Add new enemies
        if len(enemies) < 8:
            enemies.append(create_enemy())

        # Increment points every half second
        if current_time - last_point_time > POINT_INTERVAL:
            player_points += 1
            last_point_time = current_time

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw enemies
        for enemy in enemies:
            enemy_surface = pygame.Surface((ENEMY_RADIUS * 2, ENEMY_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(enemy_surface, (*ENEMY_COLOR, enemy[4]), (ENEMY_RADIUS, ENEMY_RADIUS), ENEMY_RADIUS)
            screen.blit(enemy_surface, (enemy[0] - ENEMY_RADIUS, enemy[1] - ENEMY_RADIUS))

        # Draw defenses
        for defense in defenses:
            pygame.draw.rect(screen, DEFENSE_COLOR, (0, defense[0], DEFENSE_WIDTH, DEFENSE_HEIGHT))

        # Draw points
        font = pygame.font.SysFont("monospace", 35)
        points_text = font.render(f"Points: {player_points}", True, (255, 255, 255))
        screen.blit(points_text, (10, 10))

        # Draw lives
        draw_hearts(screen, SCREEN_WIDTH - (INITIAL_LIVES + 1) * (HEART_WIDTH + 5), 20, player_lives)

        # Draw medals based on elapsed time
        elapsed_time = current_time - start_time
        if elapsed_time >= GOLD_MEDAL_TIME:
            screen.blit(GOLD_MEDAL_IMAGE, (SCREEN_WIDTH // 2 - GOLD_MEDAL_IMAGE.get_width() // 2, 20))
        elif elapsed_time >= SILVER_MEDAL_TIME:
            screen.blit(SILVER_MEDAL_IMAGE, (SCREEN_WIDTH // 2 - SILVER_MEDAL_IMAGE.get_width() // 2, 20))
        elif elapsed_time >= BRONZE_MEDAL_TIME:
            screen.blit(BRONZE_MEDAL_IMAGE, (SCREEN_WIDTH // 2 - BRONZE_MEDAL_IMAGE.get_width() // 2, 20))

        # Update the display
        pygame.display.flip()

        # Frame rate control
        clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()