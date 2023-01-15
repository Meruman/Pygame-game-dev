import pygame
import random
import asyncio

pygame.init()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Sea monsters assault")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set Game values
running = True


#Set Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#Define Classes

class GameManager():
    """ Control and update gameplay """
    def __init__(self, player, monster_group, player_bullet_group, monster_bullet_group):
        self.round_number = 1
        self.score = 0

        self.player = player
        self.monster_group = monster_group
        self.player_bullet_group = player_bullet_group
        self.monster_bullet_group = monster_bullet_group

        #Set sound and music
        self.next_level = pygame.mixer.Sound("Assets/next_level.wav")
        self.breach = pygame.mixer.Sound("Assets/breach.wav")
        self.breach.set_volume(0.6)
        self.monster_hit = pygame.mixer.Sound("Assets/monster_hit.wav")
        self.monster_hit.set_volume(0.5)
        self.player_hit = pygame.mixer.Sound("Assets/player_hit.wav")

        #Set font
        self.font = pygame.font.Font("Assets/Facon.ttf",32)

        #Set images
        Monster0 = pygame.image.load("Assets/octopus_monster.png")
        Monster1 = pygame.image.load("Assets/anglerfish.png")
        Monster2 = pygame.image.load("Assets/kraken.png")
        Monster3 = pygame.image.load("Assets/octopus2_monster.png")
        Monster4 = pygame.image.load("Assets/sea_serpent.png")
        Monster5 = pygame.image.load("Assets/squids.png")

        self.target_monster_images = [Monster0,Monster1,Monster2,Monster3,Monster4,Monster5]
        
    async def update(self):
        await self.shift_monsters()
        await self.check_collisions()
        await self.check_round_completion()

    def draw(self):
        """ Draw the HUD and other info to display """
        score_text = self.font.render(f"Score: {self.score}",True,BLACK)
        score_rect = score_text.get_rect()
        score_rect.centerx = WINDOW_WIDTH//2
        score_rect.top = 10

        round_text = self.font.render(f"Round: {self.round_number}",True,BLACK)
        round_rect = round_text.get_rect()
        round_rect.topleft = (20,10)

        lives_text = self.font.render(f"Lives: {self.player.lives}",True,BLACK)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 20,10)

        #Blit the HUD
        display_surface.blit(score_text,score_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(lives_text,lives_rect)
        pygame.draw.line(display_surface,BLACK,(0,50),(WINDOW_WIDTH,50),3)
        pygame.draw.line(display_surface,BLACK,(0,WINDOW_HEIGHT-100),(WINDOW_WIDTH,WINDOW_HEIGHT-100),3)


    async def shift_monsters(self):
        """ Shift a wave of monsters down the screen and reverse direction """
        shift = False 
        for sea_monster in self.monster_group:
            if sea_monster.rect.left <=0 or sea_monster.rect.right >= WINDOW_WIDTH:
                shift = True
                break
        if shift:
            breach = False
            for sea_monster in self.monster_group:
                sea_monster.rect.y += 10*self.round_number
                sea_monster.direction *= -1
                sea_monster.rect.x += sea_monster.direction * sea_monster.velocity
                if sea_monster.rect.bottom >= WINDOW_HEIGHT -100:
                    breach = True
            
            if breach:
                self.breach.play()
                self.player.lives -= 1
                await self.check_game_status("Sea monsters breached the line", "Press 'ENTER' to continue")


    async def check_round_completion(self):
        """ check to see if a player has completed a single round """
        if not self.monster_group:
            self.score += 1000*self.round_number
            self.round_number += 1

            await self.start_new_round()
        
    async def check_collisions(self):
        #See if any player bullet hit an alien
        if pygame.sprite.groupcollide(self.player_bullet_group, self.monster_group,True,True):
            self.monster_hit.play()
            self.score += 100

        #See if player collided with monster bullets
        if pygame.sprite.spritecollide(self.player,self.monster_bullet_group,True):
            self.player_hit.play()
            self.player.lives -= 1
            await self.check_game_status("You have been hit", "Press 'ENTER' to continue")

    async def start_new_round(self):
        #Create Monsters 11 columns and 5 rows
        for i in range(11):
            for j in range(5):
                monster = Monsters(64 + i*64, 64 + j*64, self.round_number, self.monster_bullet_group, self.target_monster_images[random.randint(0,5)])
                self.monster_group.add(monster)

        #Pause the game and prompt the user to start
        self.next_level.play()
        await self.pause_game(f"Sea monsters Assault Round {self.round_number}", "Press 'ENTER' to continue")
    async def check_game_status(self, main_text, sub_text):
        """ Check the status of the game and how the player died """
        #Empty bullet group and reset player and remaining monsters
        self.monster_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for sea_monster in self.monster_group:
            sea_monster.reset()

        #Check if the game is over or is a reset
        if self.player.lives <=0:
            await self.reset_game()
        else:
            await self.pause_game(main_text, sub_text)

    async def pause_game(self, main_text, sub_text):
        global running
        main_text = self.font.render(main_text,True,WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        sub_text = self.font.render(sub_text,True,WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Blit the text
        display_surface.fill(BLACK)
        display_surface.blit(main_text,main_rect)
        display_surface.blit(sub_text,sub_rect)
        pygame.display.update()

        #Pause the game until the user hits enter
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
            await asyncio.sleep(0)

    async def reset_game(self):
        await self.pause_game(f"Final score: {self.score}","Press 'ENTER' to continue")

        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        self.monster_group.empty()
        self.monster_bullet_group.empty()
        self.player_bullet_group.empty()
        await self.start_new_round()


class Player(pygame.sprite.Sprite):
    def __init__(self, bullets_group):
        super().__init__()
        self.image = pygame.image.load("Assets/submarine.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT-10

        self.lives = 5
        self.velocity = 8

        self.bullet_group = bullets_group

        self.shoot_sound = pygame.mixer.Sound("Assets/player_fire.wav")
        self.shoot_sound.set_volume(0.5)
        
    def update(self):
        keys = pygame.key.get_pressed()
        self.image = pygame.image.load("Assets/submarine.png")
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
            self.image = pygame.image.load("Assets/submarine_left.png")
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
            self.image = pygame.image.load("Assets/submarine_right.png")
    def fire(self):
        if len(self.bullet_group) < 3:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx,self.rect.top,self.bullet_group)
    def reset(self):
        """ Reset player position """
        self.rect.centerx = WINDOW_WIDTH//2

class Monsters(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, bullet_group, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.start_x = x
        self.start_y = y

        self.direction = 1
        self.bullet_group = bullet_group
        self.velocity = velocity

        self.shoot_sound = pygame.mixer.Sound("Assets/monster_fire.wav")
        self.shoot_sound.set_volume(0.1)

    def update(self):
        self.rect.x += self.direction * self.velocity
        if random.randint(0,1000) > 999 and len(self.bullet_group) < 3:
            self.shoot_sound.play()
            self.fire()
    def fire(self):
        MonsterBullet(self.rect.centerx,self.rect.bottom,self.bullet_group)
    def reset(self):
        self.rect.topleft = (self.start_x,self.start_y)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x,y,bullet_group):
        super().__init__()
        self.image = pygame.image.load("Assets/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.velocity = 10
        bullet_group.add(self)
    
    def update(self):
        self.rect.y -= self.velocity

        if self.rect.bottom <0:
            self.kill()

class MonsterBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Assets/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.velocity = 10
        bullet_group.add(self)
        
    
    def update(self):
        self.rect.y += self.velocity

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

#Create bullets
player_bullets_group = pygame.sprite.Group()
monster_bullets_group = pygame.sprite.Group()

#Create player group and Player
player_group = pygame.sprite.Group()
my_player = Player(player_bullets_group)
player_group.add(my_player)

#Create monster group
monsters_group = pygame.sprite.Group()

#Create the game manager
game_manager = GameManager(my_player,monsters_group, player_bullets_group, monster_bullets_group)

async def main():
    global running
    await game_manager.start_new_round()
    background_image = pygame.image.load("Assets/water_background.png")
    background_rect = background_image.get_rect()
    background_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    my_player.fire()

        display_surface.blit(background_image,background_rect)

        player_group.update()
        player_group.draw(display_surface)

        monsters_group.update()
        monsters_group.draw(display_surface)

        player_bullets_group.update()
        player_bullets_group.draw(display_surface)

        monster_bullets_group.update()
        monster_bullets_group.draw(display_surface)

        await game_manager.update()
        game_manager.draw()

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())