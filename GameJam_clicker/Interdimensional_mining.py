import pygame
import random

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Interdimensional Mining")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set game values
current_dimension = 0
resources = 0

#Set colors
GREEN = (99, 169, 81)
DARKGREEN = (47, 67, 33)

WISTERIA = (151, 81, 169)
DARKWISTERIA = (67, 41, 84)
SANTAFE = (169, 107, 81)
DARKSANTAFE = (80, 46, 39)


#Set fonts

#Set text

#Set sounds and music

#Set images
dimension = ["Dimension1", "Dimension2","Dimension3"]
dimension_index = 0
background_image = pygame.image.load(fr"GameJam_clicker\Assets\{dimension[dimension_index]}.png")
background_rect = background_image.get_rect()
background_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]
            dimension_index += 1
            if dimension_index >= len(dimension):
                dimension_index = 0
            background_image = pygame.image.load(fr"GameJam_clicker\Assets\{dimension[dimension_index]}.png")

            """ if lion_rect.collidepoint(click_x,click_y):
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
                player_lives -= 1 """


    #Blit background
    display_surface.blit(background_image,background_rect)

    #Blit HUD

    #Blit assets

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()