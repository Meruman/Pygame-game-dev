import pygame
import random
import asyncio
import os
import sys

pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath()))
    return os.path.join(base_path, relative_path)

WINDOW_WIDTH = 950
WINDOW_HEIGHT = 633
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Lion!")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 5
LION_START_VELOCITY = 3
LION_ACCELERATION = 0.5

score = 0
player_lives = PLAYER_STARTING_LIVES

lion_velocity = LION_START_VELOCITY
lion_dx = random.choice([-1,1])
lion_dy = random.choice([-1,1])


#Set colors
GREEN = (99, 169, 81)
DARKGREEN = (47, 67, 33)

WISTERIA = (151, 81, 169)
DARKWISTERIA = (67, 41, 84)
SANTAFE = (169, 107, 81)
DARKSANTAFE = (80, 46, 39)
print("Current directory: ")
print(os.getcwd())
print("Files: ")
print(os.listdir(os.getcwd()))

print("Files in Assets: ")
print(os.listdir(f"{os.getcwd()}/Assets"))


#Set fonts
custom_font = pygame.font.Font(r"Assets/XmasLights.ttf", 64)
snow_font = pygame.font.Font("Assets/DelightSnow.ttf", 32)

#Set text
title_text = custom_font.render("Catch the Penguin!!", True,WISTERIA,DARKWISTERIA)
title_rect = title_text.get_rect()
title_rect.topleft = (10,10)

score_text = snow_font.render(f"Score: {score}", True,SANTAFE,DARKSANTAFE)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH-50,10)

lives_text = snow_font.render(f"Lives: {player_lives}", True,SANTAFE,DARKSANTAFE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH-50,62)


game_over_text = custom_font.render(f"GAME OVER", True,GREEN,DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

continue_text = snow_font.render(f"Click anywhere to play again", True,GREEN,DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2 + 64)

#Set sounds and music
click_sound = pygame.mixer.Sound("Assets/click.wav")

missed_sound = pygame.mixer.Sound("Assets/quick_missed.wav")
missed_sound.set_volume(0.3)

pygame.mixer.music.load("Assets/Background_music.mp3")
pygame.mixer.music.play(-1,0,0)
pygame.mixer.music.set_volume(0.2)

#Set images
lion_image = pygame.image.load("Assets/Baby-Lion-Christmas_medium.png")
lion_rect = lion_image.get_rect()
lion_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

background_image = pygame.image.load("Assets/Background_small.png")
background_rect = background_image.get_rect()
background_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

async def main():
    global score
    global player_lives
    global lion_velocity
    global lion_dx 
    global lion_dy 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x = event.pos[0]
                click_y = event.pos[1]
    
                if lion_rect.collidepoint(click_x,click_y):
                    click_sound.play()
                    score += 1
    
                    #Increase lion speed
                    lion_velocity += LION_ACCELERATION
    
                    #Change lion direction
                    previous_dx = lion_dx
                    previous_dy = lion_dy
                    while (previous_dx == lion_dx and previous_dy == lion_dy):
                        lion_dx = random.choice([-1,1])
                        lion_dy = random.choice([-1,1])
                else:
                    missed_sound.play()
                    player_lives -= 1
    
    
        #Lion movement
        lion_rect.x += lion_dx * lion_velocity
        lion_rect.y += lion_dy * lion_velocity
    
        #Set boundaries
        if lion_rect.left < 0 or lion_rect.right > WINDOW_WIDTH:
            lion_dx = -lion_dx
        if lion_rect.top < 0 or lion_rect.bottom > WINDOW_HEIGHT:
            lion_dy = -lion_dy
    
    
        #Blit background
        display_surface.blit(background_image,background_rect)
    
        #Blit HUD
        score_text = snow_font.render(f"Score: {score}", True,SANTAFE,DARKSANTAFE)
        lives_text = snow_font.render(f"Lives: {player_lives}", True,SANTAFE,DARKSANTAFE)
        display_surface.blit(title_text,title_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(lives_text,lives_rect)
    
        #Blit assets
        display_surface.blit(lion_image,lion_rect)
    
        if player_lives <=0:
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
                        player_lives = PLAYER_STARTING_LIVES
    
                        lion_velocity = LION_START_VELOCITY
                        lion_dx = random.choice([-1,1])
                        lion_dy = random.choice([-1,1])
                        lion_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
                        pygame.mixer.music.play(-1,0,0)
                        is_paused = False
                await asyncio.sleep(0)
    
    
        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())