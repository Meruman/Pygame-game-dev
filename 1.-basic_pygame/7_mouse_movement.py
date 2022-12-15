import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Mouse movement")

#Load images
dragon_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Right\1L cien.png")
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.topleft = (25,25)


running = True
#dragging = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            dragon_image_rect.centerx = mouse_x
            dragon_image_rect.centery = mouse_y
            #dragging = True
            """ elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False """

            """ #Drag the object when the mouse button is clicked
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x = event.pos[0]
                    mouse_y = event.pos[1]
                    dragon_image_rect.centerx = mouse_x
                    dragon_image_rect.centery = mouse_y """
        
        #Drag the object when the mouse button is clicked other way
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            dragon_image_rect.centerx = mouse_x
            dragon_image_rect.centery = mouse_y
            

    #Fill the display surface to cover old images
    display_surface.fill((0,0,0))

    display_surface.blit(dragon_image,dragon_image_rect)
    pygame.display.update()

pygame.quit()