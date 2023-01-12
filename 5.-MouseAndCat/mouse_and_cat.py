import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Mouse and Cat")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set Game values
PLAYER_STARTING_LIVES = 5
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_MOUSE_VELOCITY = 3
MOUSE_ACCELERATION = 0.25
BUFFER_DISTANCE = 100

score = 0
mouse_points = 0
mouse_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL
mouse_velocity = STARTING_MOUSE_VELOCITY

#Set Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARKRED = (150,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)

#Set Fonts
custom_font = pygame.font.Font("5.-MouseAndCat\Assets\AAhaWow-2O1K8.ttf",24)

#Set Text
points_text = custom_font.render(f"Mouse points: {mouse_points}", True, RED,DARKRED)
points_rect = points_text.get_rect()
points_rect.topleft = (10,10)

score_text = custom_font.render(f"Score: {score}",True,RED,DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10,50)

title_text = custom_font.render(f"Mouse and Cat",True,RED,DARKRED)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

eaten_text = custom_font.render(f"Mouse catched: {mouse_eaten}",True,RED,DARKRED)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOW_WIDTH//2
eaten_rect.y = 50

lives_text = custom_font.render(f"Lives: {player_lives}",True,RED,DARKRED)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10,10)

boost_text = custom_font.render(f"Boost: {boost_level}",True,RED,DARKRED)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10,50)

game_over_text = custom_font.render(f"FINAL SCORE: {score}",True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = custom_font.render(f"click anywhere to play again",True, RED)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sounds and music
cat_sound = pygame.mixer.Sound("5.-MouseAndCat\Assets\miau.wav")
mouse_sound = pygame.mixer.Sound("5.-MouseAndCat\Assets\yeah-mouse-squirrel-cartoon.wav")

pygame.mixer.music.load("5.-MouseAndCat\Assets\8bit-chase-music-background.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1,0,0)

#Set images
cat_image_left = pygame.image.load("5.-MouseAndCat\Assets\cat_left.png")
cat_image_right = pygame.image.load("5.-MouseAndCat\Assets\cat_right.png")
cat_image = cat_image_left
cat_rect = cat_image.get_rect()
cat_rect.centerx = WINDOW_WIDTH//2
cat_rect.bottom = WINDOW_HEIGHT
mouse_image = pygame.image.load("5.-MouseAndCat\Assets\mouse_small.png")
mouse_rect = mouse_image.get_rect()
mouse_rect.topleft = (random.randint(0,WINDOW_WIDTH-32), -BUFFER_DISTANCE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and cat_rect.left > 0:
        cat_rect.x -= player_velocity
        cat_image = cat_image_left
    if keys[pygame.K_RIGHT] and cat_rect.right < WINDOW_WIDTH:
        cat_rect.x += player_velocity
        cat_image = cat_image_right
    if keys[pygame.K_UP] and cat_rect.top > 100:
        cat_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and cat_rect.bottom < WINDOW_HEIGHT:
        cat_rect.y += player_velocity
    
    #Engage boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level-=1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY
        
    #Move the mouse and update mouse points
    mouse_rect.y += mouse_velocity
    mouse_points = int(mouse_velocity * (WINDOW_HEIGHT - mouse_rect.y + 100))

    #Player missed the mouse
    if mouse_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        mouse_sound.play()

        mouse_rect.topleft = (random.randint(0,WINDOW_WIDTH-32), -BUFFER_DISTANCE)
        mouse_velocity = STARTING_MOUSE_VELOCITY

        cat_rect.centerx = WINDOW_WIDTH//2
        cat_rect.bottom = WINDOW_HEIGHT
        boost_level = STARTING_BOOST_LEVEL

    #Check for collisions
    if cat_rect.colliderect(mouse_rect):
        score += mouse_points
        mouse_eaten += 1
        cat_sound.play()

        mouse_rect.topleft = (random.randint(0,WINDOW_WIDTH-32), -BUFFER_DISTANCE)
        mouse_velocity += MOUSE_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

    display_surface.fill(BLACK)

    #Blit HUD
    points_text = custom_font.render(f"Mouse points: {mouse_points}", True, RED,DARKRED)
    display_surface.blit(points_text,points_rect)
    score_text = custom_font.render(f"Score: {score}",True,RED,DARKRED)
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    eaten_text = custom_font.render(f"Mouse catched: {mouse_eaten}",True,RED,DARKRED)
    display_surface.blit(eaten_text,eaten_rect)
    lives_text = custom_font.render(f"Lives: {player_lives}",True,RED,DARKRED)
    display_surface.blit(lives_text,lives_rect)
    boost_text = custom_font.render(f"Boost: {boost_level}",True,RED,DARKRED)
    display_surface.blit(boost_text,boost_rect)
    pygame.draw.line(display_surface,WHITE,(0,84),(WINDOW_WIDTH,84))

    if player_lives <=0:
        game_over_text = custom_font.render(f"FINAL SCORE: {score}",True, RED)
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    mouse_points = 0
                    mouse_eaten = 0

                    player_lives = PLAYER_STARTING_LIVES
                    player_velocity = PLAYER_NORMAL_VELOCITY

                    boost_level = STARTING_BOOST_LEVEL
                    mouse_velocity = STARTING_MOUSE_VELOCITY
                    
                    pygame.mixer.music.play(-1,0,0)
                    is_paused = False

    #Blit assets
    display_surface.blit(cat_image,cat_rect)
    display_surface.blit(mouse_image, mouse_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()