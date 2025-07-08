from item import treasures,regularShop
import pygame
from reso import resource_path
from menu import displayText 
import random
pygame.init()

def Shop(window, player):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    prices = [50,100,150]
    
    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()

        now = pygame.time.get_ticks()

        window.blit(bg, bg.get_rect())
        window.blit(cursor, mousePos)

        for i, item in enumerate(regularShop):
            x = 90 + i * 200  
            y = 40

            if item.icon:
                window.blit(pygame.transform.scale(item.icon,(64,64)), (x, y))
            rect = displayText(window, item.name, (x, y + 70), myFont, (0, 0, 0))
            if(rect.collidepoint(mousePos)):
                displayText(window,f"{item.description}",mousePos,myFont,(0,0,0))
                if(mousePressed[2] and player.gold >= prices[i]):
                    player.gold -= prices[i]
                    if(item in player.inventory.keys()):
                        player.inventory[item]+=1
                    else:
                        player.inventory[item] = 1
            displayText(window,f"{prices[i]}",(x+25,y+90),myFont,(0,0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "game"

        pygame.display.update()
        clock.tick(60)
