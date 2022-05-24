import pygame
from pygame import mixer
import math
import random

# inicjalizacja pygame
pygame.init()

# tworzenie ekranu
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# nazwa i ikona
pygame.display.set_caption("Game")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# gracz
playerImg = pygame.image.load('player.png')
playerX = 400
playerY = 500
playerX_change = 0
playerY_change = 0

# wróg
enemyImg = pygame.image.load('enemy.png')
enemyX = 1
enemyY = 1
enemyX_change = 0.3
enemyY_change = 50

# pocisk
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 20)
fontBig = pygame.font.Font('freesansbold.ttf', 60)
textX = 10
textY = 10

gameoverX = 250
gameoverY = 250


def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_value, (x, y))


def show_game_over(x, y):
    game_over = fontBig.render("GAME OVER", True, (0, 0, 0))
    screen.fill((0, 255, 0))
    screen.blit(game_over, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # left, right, up or down?
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('sound.wav')
                    bullet_Sound.play()
                    bullet_Sound.set_volume(0.1)
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # borders for player X coordinate
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    if enemyY > 500:
        show_game_over(gameoverX, gameoverY)

    # borders for player Y coordinate
    if playerY <= 0:
        playerY = 0
    elif playerY >= 568:
        playerY = 568

    enemyX += enemyX_change
    # borders for enemy X coordinate
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -enemyX_change
        enemyY += enemyY_change

    # bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        explosion_Sound = mixer.Sound('explosion.wav')
        explosion_Sound.play()
        explosion_Sound.set_volume(1)
        bulletY = 450
        bullet_state = "ready"
        score += 1
        enemyX = 1
        enemyY = 1
        enemyX_change += 1

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)
    pygame.display.update()