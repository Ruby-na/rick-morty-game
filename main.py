import pygame
import sys

pygame.init()
pygame.mixer.init()

# Screen
WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rick Portal Escape")

clock = pygame.time.Clock()

# Colors
SKY = (80, 180, 255)
GROUND = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
PURPLE = (150, 0, 200)
BLACK = (0, 0, 0)

# Sounds
jump_sound = pygame.mixer.Sound("assets/sounds/jump.ogg")
coin_sound = pygame.mixer.Sound("assets/sounds/coin.wav")
hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")

# Player
player_w = 80
player_h = 80
player_x = 100
player_y = 300

speed = 5

# Physics
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = False

# Game state
score = 0
game_over = False

# Load Rick
rick = pygame.image.load("assets/rick.png.png")
rick = pygame.transform.scale(rick, (player_w, player_h))

# Spikes
spikes = [
    pygame.Rect(400, 360, 40, 40),
    pygame.Rect(650, 360, 40, 40),
]

# Collectibles
seeds = [
    pygame.Rect(300, 320, 25, 25),
    pygame.Rect(550, 280, 25, 25),
]

# Enemy
enemy = pygame.Rect(500, 360, 40, 40)
enemy_dir = 1

# Portal (finish)
portal = pygame.Rect(800, 300, 60, 100)

def reset_game():
    global player_x, player_y, velocity_y, score, game_over
    player_x = 100
    player_y = 300
    velocity_y = 0
    score = 0
    game_over = False

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Jump
            if event.key == pygame.K_SPACE and on_ground and not game_over:
                velocity_y = jump_power
                jump_sound.play()

            # Restart
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= speed

        if keys[pygame.K_RIGHT]:
            player_x += speed

        # Gravity
        velocity_y += gravity
        player_y += velocity_y

        # Ground collision
        if player_y >= 320:
            player_y = 320
            velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)

        # Enemy movement
        enemy.x += enemy_dir * 3
        if enemy.x > 700 or enemy.x < 300:
            enemy_dir *= -1

        # Spike collision
        for spike in spikes:
            if player_rect.colliderect(spike):
                game_over = True
                hit_sound.play()

        # Enemy collision
        if player_rect.colliderect(enemy):
            game_over = True
            hit_sound.play()

        # Collectibles
        for seed in seeds[:]:
            if player_rect.colliderect(seed):
                seeds.remove(seed)
                score += 1
                coin_sound.play()

        # Portal win
        if player_rect.colliderect(portal):
            game_over = True

    # DRAW
    screen.fill(SKY)

    # Ground
    pygame.draw.rect(screen, GROUND, (0, 400, WIDTH, 100))

    # Spikes
    for spike in spikes:
        pygame.draw.rect(screen, RED, spike)

    # Seeds
    for seed in seeds:
        pygame.draw.rect(screen, YELLOW, seed)

    # Enemy
    pygame.draw.rect(screen, BLACK, enemy)

    # Portal
    pygame.draw.rect(screen, PURPLE, portal)

    # Player
    screen.blit(rick, (player_x, player_y))

    # Score
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    # Game Over
    if game_over:
        msg = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(msg, (250, 200))

    pygame.display.update()
    clock.tick(60)