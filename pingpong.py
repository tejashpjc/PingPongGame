import pygame
import random

# to initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 6
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10
POWER_UP_SIZE = 15
POWER_UP_DURATION = 5000 #MILLISECONDS

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

COLORS = {"Red": RED, "Blue": BLUE, "Green": GREEN, "Yellow": YELLOW}

#  select paddle color
def select_color():
    print("Choose paddle color:")
    for i, color in enumerate(COLORS.keys(), start=1):
        print(f"{i}. {color}")
    choice = int(input("Enter number: ")) - 1
    return list(COLORS.values())[choice]

paddle_color = select_color()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle and Ball positions
player1_y, player2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2, HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED * random.choice([1, -1]), BALL_SPEED * random.choice([1, -1])

# Power-up variables
power_up_x, power_up_y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
power_up_active = False
power_up_start_time = 0
power_up_effect = "none"

# Game loop
running = True
while running:
    pygame.time.delay(16)  # ~60 FPS
    screen.fill(BLACK)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_y < HEIGHT - PADDLE_HEIGHT:
        player1_y += PADDLE_SPEED
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player2_y < HEIGHT - PADDLE_HEIGHT:
        player2_y += PADDLE_SPEED

    # Ball Movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball Collision with Top/Bottom
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1

    # Ball Collision with Paddles
    if (ball_x <= PADDLE_WIDTH and player1_y <= ball_y <= player1_y + PADDLE_HEIGHT) or \
       (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and player2_y <= ball_y <= player2_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Ball Out of Bounds (Reset)
    if ball_x < 0 or ball_x > WIDTH:
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = BALL_SPEED * random.choice([1, -1]), BALL_SPEED * random.choice([1, -1])

    # Power-up spawn logic
    if not power_up_active and random.randint(0, 500) == 1:  # Random chance to spawn
        power_up_x, power_up_y = random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)
        power_up_active = True
        power_up_effect = random.choice(["speed", "slow", "invert"])

    # Check if ball hits power-up
    if power_up_active and power_up_x - BALL_SIZE < ball_x < power_up_x + POWER_UP_SIZE and \
       power_up_y - BALL_SIZE < ball_y < power_up_y + POWER_UP_SIZE:
        power_up_active = False
        power_up_start_time = pygame.time.get_ticks()
        if power_up_effect == "speed":
            BALL_SPEED += 2
        elif power_up_effect == "slow":
            BALL_SPEED = max(2, BALL_SPEED - 2)
        elif power_up_effect == "invert":
            ball_dx *= -1
            ball_dy *= -1

    # Reset power-up effect after duration
    if power_up_start_time and pygame.time.get_ticks() - power_up_start_time > POWER_UP_DURATION:
        BALL_SPEED = 5
        power_up_start_time = 0

    # Draw Paddles, Ball, and Power-ups
    pygame.draw.rect(screen, paddle_color, (0, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, paddle_color, (WIDTH - PADDLE_WIDTH, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    if power_up_active:
        pygame.draw.rect(screen, PURPLE, (power_up_x, power_up_y, POWER_UP_SIZE, POWER_UP_SIZE))

    pygame.display.update()

pygame.quit()
