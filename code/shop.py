from item import treasures,regularShop
import pygame
from reso import resource_path
from menu import displayText 
import random
pygame.init()
pygame.mixer.init()

def Shop(window, player):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    prices = [50,100,150]
    purchase = pygame.mixer.Sound(resource_path("assets/sound/cash-register-purchase-87313.mp3"))
    lastPurcahse = 0
    buyDelay = 400

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
            displayText(window, f"Gold: {player.gold}", (20, 10), myFont, (255, 215, 0))
            if(rect.collidepoint(mousePos)):
                displayText(window,f"{item.description}",mousePos,myFont,(0,0,0))
                now= pygame.time.get_ticks()
                if(mousePressed[2] and player.gold >= prices[i] and now - lastPurcahse > buyDelay):
                    lastPurcahse =now
                    player.gold -= prices[i]
                    purchase.play()
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
