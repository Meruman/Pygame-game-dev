import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Blitting text")

#Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

#See all available system fonts
fonts = pygame.font.get_fonts()
""" for font in fonts:
    print(font) """

#Define fonts
system_font = pygame.font.SysFont('calibri',64)
custom_font = pygame.font.Font("1.-basic_pygame\sunny-spells-font\SunnyspellsRegular-MV9ze.otf",64)

#Define text
system_text = system_font.render("Dragons are the best!",True, GREEN, DARKGREEN)
system_text_rect = system_text.get_rect()
system_text_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

custom_text = custom_font.render("Move the dragon!!", True, GREEN)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Blit (Copy) text surfaces to the display
    display_surface.blit(system_text,system_text_rect)
    display_surface.blit(custom_text,custom_text_rect)
    pygame.display.update()

pygame.quit()