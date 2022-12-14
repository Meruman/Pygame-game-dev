import pygame

#Initialiye pygame
pygame.init()

#Create a display surface and set its caption
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Adding sounds")

#Load sound effects
sound_1 = pygame.mixer.Sound("1.-basic_pygame\Sounds\paper-rustle-and-plop-on-wooden-table.wav")
sound_2 = pygame.mixer.Sound("1.-basic_pygame\Sounds\camera-shutter-lens.wav")

#Play sound effects
sound_1.play()
pygame.time.delay(int(3000 + 1000))
sound_2.play()
pygame.time.delay(int(3000))

#Change volume of sound effect
sound_1.set_volume(1.5)
sound_1.play()


#Load background music
pygame.mixer.music.load("1.-basic_pygame\Sounds\lofi-melody-loop.wav")

#Play and stop the music
pygame.mixer.music.play(-1,0,0)
pygame.time.delay(5000)
pygame.mixer.music.stop()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()