import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Continuous movement")

#Load images
dragon_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Right\1L cien.png")
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
VELOCITY = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        dragon_image_rect.x -= VELOCITY
    if keys[pygame.K_RIGHT]:
        dragon_image_rect.x += VELOCITY
    if keys[pygame.K_DOWN]:
        dragon_image_rect.y += VELOCITY
    if keys[pygame.K_UP]:
        dragon_image_rect.y -= VELOCITY
        

    #Fill the display surface to cover old images
    display_surface.fill((0,0,0))

    display_surface.blit(dragon_image,dragon_image_rect)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()