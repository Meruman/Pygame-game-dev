import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Keyboard movement")


#Set game values
VELOCITY = 10

#Load images
dragon_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Right\1L cien.png")
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.centerx = WINDOW_WIDTH//2
dragon_image_rect.bottom = WINDOW_HEIGHT


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dragon_image_rect.x -= VELOCITY
            if event.key == pygame.K_RIGHT:
                dragon_image_rect.x += VELOCITY
            if event.key == pygame.K_DOWN:
                dragon_image_rect.y += VELOCITY
            if event.key == pygame.K_UP:
                dragon_image_rect.y -= VELOCITY

    #Fill the display surface to cover old images
    display_surface.fill((0,0,0))

    display_surface.blit(dragon_image,dragon_image_rect)
    pygame.display.update()

pygame.quit()