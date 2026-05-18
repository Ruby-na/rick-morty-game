import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rick and Morty Game")

WHITE = (255, 255, 255)
BLUE = (80, 180, 255)

player_x = 100
player_y = 200
player_size = 50
speed = 5

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= speed

    if keys[pygame.K_RIGHT]:
        player_x += speed

    if keys[pygame.K_UP]:
        player_y -= speed

    if keys[pygame.K_DOWN]:
        player_y += speed

    screen.fill(BLUE)

    pygame.draw.rect(
        screen,
        WHITE,
        (player_x, player_y, player_size, player_size)
    )

    pygame.display.update()
    clock.tick(60)