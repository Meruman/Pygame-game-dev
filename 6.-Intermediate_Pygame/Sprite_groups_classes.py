import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Groups")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set Game values

#Set Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DARKRED = (150,0,0)
GREEN = (0,255,0)
DARKGREEN = (10,50,10)

class GameManager():
    def __init__(self, enemy_group, player_group):
        self.enemy_group = enemy_group
        self.player_group = player_group
    def update(self):
        self.player_group.update()
        self.enemy_group.update()
        self.check_collisions()
    def check_collisions(self):
        pygame.sprite.groupcollide(self.enemy_group,self.player_group,True,False)
        

#Define classes
class Monster(pygame.sprite.Sprite):
    """ A spookie monster """
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load(r"6.-Intermediate_Pygame\Assets\mouse.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = random.randint(1,5)

    def update(self):
        self.rect.y += self.velocity

class Player(pygame.sprite.Sprite):
    """ Player class """
    def __init__(self, x,y, enemies_group):
        super().__init__()
        self.image = pygame.image.load(r"6.-Intermediate_Pygame\Assets\Baby-Lion-Christmas_medium.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.velocity = 5
        self.enemies_group = enemies_group

    def update(self):
        self.move()
        #self.check_collisions()

    def move(self):
        """ Move continously the player """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.velocity

    """ def check_collisions(self):
        #Check for collisions between the player and another sprite group
        if pygame.sprite.spritecollide(self,self.enemies_group,True):
            print(len(self.enemies_group)) """

#Create 10 monsters and group them
monster_group = pygame.sprite.Group()
for i in range(10):
    monster = Monster(i*64, 10)
    monster_group.add(monster)

#Create player group and add player
player_group = pygame.sprite.Group()
player_group.add(Player(500,500,monster_group))

#Create a Game manager object
game_manager = GameManager(monster_group,player_group)

#Set Fonts

#Set Text

#Set sounds and music


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.fill((0,0,0))
    game_manager.update()
    player_group.draw(display_surface)
    monster_group.draw(display_surface)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()