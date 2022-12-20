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

#Set sounds and music
cat_sound = pygame.mixer.Sound("5.-MouseAndCat\Assets\miau.wav")
mouse_sound = pygame.mixer.Sound("5.-MouseAndCat\Assets\yeah-mouse-squirrel-cartoon.wav")

pygame.mixer.music.load("5.-MouseAndCat\Assets\8bit-chase-music-background.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1,0,0)

#Set images
cat_image = pygame.image.load("5.-MouseAndCat\Assets\cat_left.png")
mouse_image = pygame.image.load("5.-MouseAndCat\Assets\mouse_small.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        


    #Blit HUD
    display_surface.blit(points_text,points_rect)
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(eaten_text,eaten_rect)
    display_surface.blit(lives_text,lives_rect)
    display_surface.blit(boost_text,boost_rect)
    pygame.draw.line(display_surface,WHITE,(0,84),(WINDOW_WIDTH,84))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()