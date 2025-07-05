import pygame
from reso import resource_path
from mnst import Monster
from mnst import loadMonsterAssets
from mnst import handleMonster
from bg import Background

pygame.init()

#stting vars
winSize = (640,380)
window = pygame.display.set_mode(winSize)
clock = pygame.time.Clock()
run  = True

#loading shit
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))
cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
mnsAssets = loadMonsterAssets(resource_path("assets/mns"))
monsters = []
pygame.mouse.set_visible(False)

while run:
    mousePoS = pygame.mouse.get_pos()
    window.blit(bg,bg.get_rect()) #drawing battle box
    window.blit(cursor,mousePoS)

    for event in pygame.event.get(): #basic event handling
        if(event.type == pygame.QUIT):
            run = False

    for mns in monsters:
        handleMonster(mns,window)

    pygame.display.update() #updating screen each frame
    clock.tick(60)