import pygame
from reso import resource_path
from mnst import Monster
pygame.init()

#stting vars
winSize = (640,380)
window = pygame.display.set_mode(winSize)
clock = pygame.time.Clock()
run  = True

#loading shit
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))

while run:
    window.blit(bg,bg.get_rect()) #drawing bg

    for event in pygame.event.get(): #basic event handling
        if(event.type == pygame.QUIT):
            run = False


    pygame.display.update() #updating screen each frame
    clock.tick(60)