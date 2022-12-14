import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Blitting images")

#Create images... returns a surface object with the image drawn on it
#We can then get the rect of the surface and use the rect to position the image.

dragon_left_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Left\000.png")
dragon_left_rect = dragon_left_image.get_rect()
dragon_left_rect.topleft = (0,0)


dragon_right_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Right\1L cien.png")
dragon_right_rect = dragon_right_image.get_rect()
dragon_right_rect.topright = (WINDOW_WIDTH,0)

pygame.draw.line(display_surface,(255,255,255),(0, 70), (WINDOW_WIDTH,70),4)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Blit (copy) a surface object at a given coordinates to our display
    display_surface.blit(dragon_left_image,dragon_left_rect)
    display_surface.blit(dragon_right_image,dragon_right_rect)

    pygame.display.update()

pygame.quit()