import pygame
import random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Classic snake")

#Set tick and FPS
FPS = 20
clock = pygame.time.Clock()

#Set game values
SNAKE_SIZE = 20
SNAKE_VELOCITY = 3

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 + 100

snake_dx = 0
snake_dy = 0

score = 0

#Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARKRED = (150,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)

#Set fonts
system_font = pygame.font.SysFont("gabriola",48)

#Set text
title_text = system_font.render("s n a k e",True,GREEN,DARKGREEN)
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

score_text = system_font.render(f"Score: {score}", True,GREEN,DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

game_over_text = system_font.render("GAME OVER", True,RED,DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

continue_text = system_font.render("Press any key to play again", True,RED,DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 64)

#Set sound and music
pick_up_sound = pygame.mixer.Sound("4.-snake\Assets\pickup_item.wav")
pick_up_sound.set_volume(0.5)

#Set images
apple_coord = (500,500, SNAKE_SIZE,SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface,RED,apple_coord)

head_coord = (head_x,head_y,SNAKE_SIZE,SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface,GREEN,head_coord)

body_coords = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake_dx = -1*SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake_dx = 1*SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake_dx = 0
                snake_dy = 1*SNAKE_SIZE
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake_dx = 0
                snake_dy = -1*SNAKE_SIZE
    #Blit HUD
    display_surface.fill(WHITE)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(score_text,score_rect)

    body_coords.insert(0,head_coord)
    body_coords.pop()
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x,head_y,SNAKE_SIZE,SNAKE_SIZE)


    for body_coord in body_coords:
        pygame.draw.rect(display_surface,DARKGREEN,body_coord)
    apple_rect = pygame.draw.rect(display_surface,RED,apple_coord)
    head_rect = pygame.draw.rect(display_surface,GREEN,head_coord)

    if head_rect.left <= 0 or head_rect.top <= 0 or head_rect.bottom >= WINDOW_HEIGHT or head_rect.right >= WINDOW_WIDTH or head_coord in body_coords:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    is_paused = False
                    score = 0
                    apple_coord = (500,500, SNAKE_SIZE,SNAKE_SIZE)
                    apple_rect = pygame.draw.rect(display_surface,RED,apple_coord)
                    head_x = WINDOW_WIDTH//2
                    head_y = WINDOW_HEIGHT//2 + 100
                    head_coord = (head_x,head_y,SNAKE_SIZE,SNAKE_SIZE)
                    snake_dx = 0
                    snake_dy = 0
                    body_coords = []

    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()
        apple_coord = (random.randint(SNAKE_SIZE,WINDOW_WIDTH - SNAKE_SIZE),random.randint(SNAKE_SIZE,WINDOW_HEIGHT-SNAKE_SIZE), SNAKE_SIZE,SNAKE_SIZE)
        body_coords.append(head_coord)
    score_text = system_font.render(f"Score: {score}", True,GREEN,DARKGREEN)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()