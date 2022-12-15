import pygame
import random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Collisions!")

#Load images
dragon_image = pygame.image.load(r"1.-basic_pygame\DragonCharacter\Character\Walk\Left\000.png")
dragon_image_rect = dragon_image.get_rect()
dragon_image_rect.topleft = (25,25)

coin_image = pygame.image.load(r"1.-basic_pygame\assets\coin-icon.png")
coin_image_rect = coin_image.get_rect()
coin_image_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

VELOCITY = 5

FPS = 60
clock = pygame.time.Clock()

#Define colors as RGB tuples
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and dragon_image_rect.left > 0:
        dragon_image_rect.x -= VELOCITY
    if keys[pygame.K_d] and dragon_image_rect.right < WINDOW_WIDTH:
        dragon_image_rect.x += VELOCITY
    if keys[pygame.K_w] and dragon_image_rect.top > 0:
        dragon_image_rect.y -= VELOCITY
    if keys[pygame.K_s] and dragon_image_rect.bottom < WINDOW_HEIGHT:
        dragon_image_rect.y += VELOCITY


    if dragon_image_rect.colliderect(coin_image_rect):
        print("HIT!!")
        coin_image_rect.x = random.randint(0,WINDOW_WIDTH-coin_image.get_size()[0])
        coin_image_rect.y = random.randint(0,WINDOW_HEIGHT-coin_image.get_size()[1])
    display_surface.fill((0,0,0))
    display_surface.blit(dragon_image,dragon_image_rect)
    display_surface.blit(coin_image,coin_image_rect)

    pygame.draw.rect(display_surface,RED,dragon_image_rect, 1)
    pygame.draw.rect(display_surface,YELLOW,coin_image_rect, 1)

    pygame.display.update()

    clock.tick(FPS)


pygame.quit()