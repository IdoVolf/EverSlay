import pygame
from reso import resource_path
from mnst import Monster
from mnst import loadMonsterAssets
from mnst import handleMonster
from bg import Background
from bg import loadBackgroundAssets

pygame.init()

#stting vars
winSize = (640,380)
window = pygame.display.set_mode(winSize)
clock = pygame.time.Clock()
run  = True

#loading shit
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))
mnsAssets = loadMonsterAssets("assets/mns")
mns = Monster(mnsAssets[0],2,2,1,(48,48))

while run:
    mousePoS = pygame.mouse.get_pos()
    window.blit(bg,bg.get_rect()) #drawing battle box


    for event in pygame.event.get(): #basic event handling
        if(event.type == pygame.QUIT):
            run = False

    handleMonster(mns,window)

    pygame.display.update() #updating screen each frame
    clock.tick(60)