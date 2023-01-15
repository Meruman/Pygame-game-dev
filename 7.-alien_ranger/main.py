import pygame
import random
import asyncio

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Alien Ranger")

#Set tick and FPS
FPS = 60
clock = pygame.time.Clock()

#Set Game values
running = True

#Set Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
ALIEN0_COLOR = (234,40,0)
ALIEN1_COLOR = (251,111,12)
ALIEN2_COLOR = (94,173,191)
ALIEN3_COLOR = (254,226,0)
ALIEN4_COLOR = (158,221,125)

#Define a Game manager object
class GameManager():
    """ Class to manage the gameplay """
    def __init__(self, player, alien_group):
        self.player = player
        self.alien_group = alien_group

        self.score = 0
        self.round_number = 0

        self.round_time = 0

        #Set sounds and music
        self.next_level_sound = pygame.mixer.Sound("Assets/next_level.wav")
        self.next_level_sound.set_volume(0.5)
        """ pygame.mixer.music.load("Assets/background.wav")
        pygame.mixer.music.play(-1,0,0)
        pygame.mixer.music.set_volume(0.8) """

        #Set font
        self.font = pygame.font.Font("Assets/ApeMount-WyPM9.ttf",24)

        #Set images
        Alien0 = pygame.image.load("Assets/Alien0.png")
        Alien1 = pygame.image.load("Assets/Alien1.png")
        Alien2 = pygame.image.load("Assets/Alien2.png")
        Alien3 = pygame.image.load("Assets/Alien3.png")
        Alien4 = pygame.image.load("Assets/Alien4.png")

        self.target_alien_images = [Alien0,Alien1,Alien2,Alien3,Alien4]
        self.target_alien_type = random.randint(0,4)
        self.target_alien = self.target_alien_images[self.target_alien_type]
        self.target_alien_rect = self.target_alien.get_rect()
        self.target_alien_rect.centerx = WINDOW_WIDTH//2
        self.target_alien_rect.top = 35

        self.colors = [ALIEN0_COLOR,ALIEN1_COLOR,ALIEN2_COLOR,ALIEN3_COLOR,ALIEN4_COLOR]

    async def update(self):
        self.round_time += 1

        #Check for collisions
        await self.check_collisions()
    def draw(self):
        """ Draw the HUD and other objects """
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH//2
        catch_rect.top = 5

        score_text = self.font.render(f"Score: {self.score}",True,WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5,5)

        lives_text = self.font.render(f"Lives: {self.player.lives}",True,WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5,35)

        round_text = self.font.render(f"Current round: {self.round_number}", True,WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5,65)

        time_text = self.font.render(f"Round time: {int(self.round_time/FPS)}", True,WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10,5)

        warp_text = self.font.render(f"Warps: {self.player.warps}", True,WHITE)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10,35)        

        display_surface.blit(catch_text,catch_rect)
        display_surface.blit(score_text,score_rect)
        display_surface.blit(lives_text,lives_rect)
        display_surface.blit(round_text,round_rect)
        display_surface.blit(time_text,time_rect)
        display_surface.blit(warp_text,warp_rect)

        display_surface.blit(self.target_alien,self.target_alien_rect)
        pygame.draw.rect(display_surface, self.colors[self.target_alien_type], (self.target_alien_rect.left - 5,self.target_alien_rect.top - 5,self.target_alien_rect.width + 10,self.target_alien_rect.height + 10),2)
        pygame.draw.rect(display_surface,self.colors[self.target_alien_type],(0,110,WINDOW_WIDTH,WINDOW_HEIGHT-205),3)


    async def check_collisions(self):
        collided_alien = pygame.sprite.spritecollideany(self.player,self.alien_group)

        if collided_alien:
            if collided_alien.alien_type == self.target_alien_type:
                self.score += 100*self.round_number
                #Remove the collided alien from the group
                collided_alien.remove(self.alien_group)
                if self.alien_group:
                    #There are still more monsters
                    self.player.catch_sound.play()
                    self.choose_new_target()
                else:
                    #There are no more monsters
                    self.player.reset()
                    self.start_new_round()
            #We catched the wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                if self.player.lives <= 0:
                    await self.pause_game(f"Final score: {self.score}","Press ENTER to play again")
                    self.restart_game()
                self.player.reset()

    def start_new_round(self):
        self.next_level_sound.stop()
        self.score += int(10000*self.round_number/(1+self.round_time))

        #Reset variables
        self.round_time = 0
        self.round_number += 1
        self.alien_group.empty()
        self.player.warps += 1
        alien_number = self.round_number * 2
        for i in range(alien_number):
            self.alien_group.add(Alien(random.randint(0,WINDOW_WIDTH - 70),random.randint(110,WINDOW_HEIGHT-264),self.target_alien_images[i%5],i%5))

        #Choose a new target alien
        self.choose_new_target()
        self.next_level_sound.play()

    def choose_new_target(self):
        selected_alien = random.choice(self.alien_group.sprites())
        self.target_alien_type = selected_alien.alien_type
        self.target_alien = selected_alien.image
        self.target_alien_rect = self.target_alien.get_rect()
        self.target_alien_rect.centerx = WINDOW_WIDTH//2
        self.target_alien_rect.top = 35

    async def pause_game(self, main_text, sub_text):
        global running
        """ pygame.mixer.music.fadeout(500)
        self.next_level_sound.fadeout(100) """
        self.next_level_sound.stop()

        game_over_text = self.font.render(main_text,True,WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 35)

        continue_text = self.font.render(sub_text,True,WHITE)
        continue_rect = continue_text.get_rect()
        continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 -35 + 64)

        display_surface.fill(BLACK)
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)

        pygame.display.update()

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

    async def initial_pause_game(self, main_text, second_text, sub_text):
        global running
        """ pygame.mixer.music.fadeout(500)
        self.next_level_sound.fadeout(100) """
        self.next_level_sound.stop()

        game_over_text = self.font.render(main_text,True,WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 125)


        # Split the text into lines based on the wrap width
        lines = []
        line = ""
        for word in second_text.split():
            if self.font.size(line + " " + word)[0] <= WINDOW_WIDTH//2 + 100:
                line += " " + word
            else:
                lines.append(line)
                line = word
        lines.append(line)

        # Set the position of the text on the screen
        text_rect = pygame.Rect(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, WINDOW_WIDTH//2, len(lines)*self.font.size(second_text)[1])
        text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        """ second_text = self.font.render(second_text,True,WHITE)
        second_rect = second_text.get_rect()
        second_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) """

        continue_text = self.font.render(sub_text,True,WHITE)
        continue_rect = continue_text.get_rect()
        continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 125)

        display_surface.fill(BLACK)
        display_surface.blit(game_over_text,game_over_rect)

        # Draw the wrapped text on the screen
        y = text_rect.top
        for line in lines:
            text_surface = self.font.render(line, True, (255, 255, 255))
            display_surface.blit(text_surface, (text_rect.left, y))
            y += self.font.size(line)[1]

        display_surface.blit(continue_text,continue_rect)

        pygame.display.update()

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
                

    def restart_game(self):
        #pygame.mixer.music.play(-1,0,0)
        self.score = 0
        self.round_number = 0
        self.player.reset()
        self.player.lives = 5
        self.player.warps = 2
        self.start_new_round()
        

#Define classes
class Player(pygame.sprite.Sprite):
    """ Player class """
    def __init__(self):
        super().__init__()
        self.lives = 5
        self.warps = 2
        self.velocity = 8

        self.image = pygame.image.load("Assets/Ranger.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        self.catch_sound = pygame.mixer.Sound("Assets/catched.wav")
        self.die_sound = pygame.mixer.Sound("Assets/died.wav")
        self.warp_sound = pygame.mixer.Sound("Assets/warp.wav")

    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 110:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT-110:
            self.rect.y += self.velocity

    def warp(self):
        """ Warp the player to the safe zone """
        if self.warps > 0:
            self.warps -= 1
            self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT
    def reset(self):
        """ Reset the player position (For when it is hit) """
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

class Alien(pygame.sprite.Sprite):
    """ class for an alien """
    def __init__(self, x, y, image, alien_type):
        super().__init__()
        self.image = image
        self.alien_type = alien_type
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
        self.dx = random.choice([-1,1])
        self.dy = random.choice([-1,1])

        self.velocity = random.randint(1,5)

    def update(self):
        super().update()
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top < 110 or self.rect.bottom > WINDOW_HEIGHT-100:
            self.dy *= -1

#Create Aliens and group them
alien_group = pygame.sprite.Group()

#Create player group and add player
my_player = Player()
player_group = pygame.sprite.Group()
player_group.add(my_player)

#Create Game object
game_manager = GameManager(my_player,alien_group)

async def main():
    global running
    await game_manager.initial_pause_game("Try to catch all the aliens as fast as you can.","Use the arrow keys to move, you can warp to the safe zone with Space bar but be careful not to waste all your warps", "Press ENTER to play")
    game_manager.start_new_round()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    my_player.warp()

        display_surface.fill((0,0,0))


        alien_group.update()
        alien_group.draw(display_surface)

        await game_manager.update()
        game_manager.draw()

        player_group.update()
        player_group.draw(display_surface)

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())