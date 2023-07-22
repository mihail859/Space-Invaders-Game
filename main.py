import pygame
import random

import math
from pygame import mixer


# initialise the pygame

pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))


# Create the background

background = pygame.image.load("background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load("space_img.png")
player_x = 370
player_y = 480

player_x_change = 0


# Enemy

# Creating mulyiple enemies

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6
#

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(3)
    enemy_y_change.append(40)   




# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 23)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_txt = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_txt, (200, 250))



def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB - Green, Blue , Yellow , etc..
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_x_change = 0
    
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()

            bullet_x = player_x
            fire_bullet(bullet_x, bullet_y)
    if keys[pygame.K_LEFT]:

        player_x_change = -3        
    if keys[pygame.K_RIGHT]:

        player_x_change = 3

    # Player borders    
    player_x += player_x_change    


    if player_x <= 0:
    
       player_x = 0 

    elif player_x >= 736:

        player_x = 736   
               

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000

            game_over_text()
            
            break    




        enemy_x[i] += enemy_x_change[i]


        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2.5
            enemy_y[i] += enemy_y_change[i]

        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -2.5
            enemy_y[i] += enemy_y_change[i]

            # Collision
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)

        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()


            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)    
    

    # Bullet movement
    if  bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change  


    player(player_x, player_y)

    show_score(textX, textY)

    pygame.display.update()
     



