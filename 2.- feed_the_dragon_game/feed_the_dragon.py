import pygame
import random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Feed the dragon!")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
FOOD_STARTING_VELOCITY = 10
FOOD_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
food_velocity = FOOD_STARTING_VELOCITY

#Set colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

#Set fonts
custom_font = pygame.font.Font("2.- feed_the_dragon_game\Assets\SunnyspellsRegular-MV9ze.otf", 64)

#Set text
score_text = custom_font.render(f"Score: {score}",True,GREEN,DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = custom_font.render(f"Feed the dragon!!", True,GREEN)
title_rect = title_text.get_rect()
title_rect.top = 10 
title_rect.centerx = WINDOW_WIDTH//2

lives_text = custom_font.render(f"Lives: {player_lives}",True,GREEN,DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH-10,10)

game_over_text = custom_font.render("GAME OVER",True,GREEN,DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

continue_text = custom_font.render("Press any key to continue",True,GREEN,DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 60)

#Set sounds and music
food_sound = pygame.mixer.Sound("2.- feed_the_dragon_game\Assets\chewing-breadstick.wav")
food_sound.set_volume(0.1)

miss_sound = pygame.mixer.Sound("2.- feed_the_dragon_game\Assets\miss-sfx.wav")
miss_sound.set_volume(0.1)

pygame.mixer.music.load("2.- feed_the_dragon_game\Assets\lofi-melody-loop.wav")
pygame.mixer.music.play(-1,0,0)
pygame.mixer.music.set_volume(0.3)

#Set images
dragon_image = pygame.image.load("2.- feed_the_dragon_game\Assets\Dragon.png")
dragon_rect = dragon_image.get_rect()
dragon_rect.left = 32
dragon_rect.centery = WINDOW_HEIGHT//2

food_image = pygame.image.load("2.- feed_the_dragon_game\Assets\Food-icon.png")
food_rect = food_image.get_rect()
food_rect.center = (WINDOW_WIDTH + BUFFER_DISTANCE,random.randint(64,WINDOW_HEIGHT - food_image.get_size()[1]))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and dragon_rect.top > 64:
        dragon_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_s] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += PLAYER_VELOCITY

    #Move food
    #Missed food
    if food_rect.left < 0:
        player_lives -= 1
        miss_sound.play()
        food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        food_rect.y = random.randint(64,WINDOW_HEIGHT - food_image.get_size()[1])
    else:
        food_rect.left -= food_velocity

    #Check collision
    if dragon_rect.colliderect(food_rect):
        score += 1
        food_sound.play()
        food_velocity += FOOD_ACCELERATION
        food_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        food_rect.y = random.randint(64,WINDOW_HEIGHT - food_image.get_size()[1])

    score_text = custom_font.render(f"Score: {score}",True,GREEN,DARKGREEN)
    lives_text = custom_font.render(f"Lives: {player_lives}",True,GREEN,DARKGREEN)

    display_surface.fill(BLACK)
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(lives_text,lives_rect)
    pygame.draw.line(display_surface,WHITE,(0,64),(WINDOW_WIDTH,64))

    display_surface.blit(dragon_image,dragon_rect)
    display_surface.blit(food_image,food_rect)

    if player_lives == 0:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    food_velocity = FOOD_STARTING_VELOCITY
                    dragon_rect.centery = WINDOW_HEIGHT//2
                    pygame.mixer.music.play(-1,0,0)
                    is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    pygame.display.update()

    clock.tick(FPS)

pygame.quit()