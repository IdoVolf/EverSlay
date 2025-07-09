from item import rare,regularShop,regularBottom
import pygame
from reso import resource_path
from menu import displayText 
import random
pygame.init()
pygame.mixer.init()

def Shop(window, player,rareN):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    prices = [100,150,200]
    purchase = pygame.mixer.Sound(resource_path("assets/sound/cash-register-purchase-87313.mp3"))
    lastPurcahse = 0
    buyDelay = 400
    rareItem  = rare[rareN]
    rareP = 200
    uniqePos = (256,190)
    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()

        now = pygame.time.get_ticks()

        window.blit(bg, bg.get_rect())

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
            window.blit(pygame.transform.scale(rareItem.icon,(64,64)),(uniqePos[0],uniqePos[1]-20))
            uniqeRect = displayText(window,f"{rareItem.name}",(uniqePos[0],uniqePos[1]-30),myFont,(255,215,100))
            displayText(window,f"{rareP}",(uniqePos[0],uniqePos[1]+30),myFont,(255,215,100))
            if(uniqeRect.collidepoint(mousePos)):
                displayText(window,f"{rareItem.description}",mousePos,myFont,(255,215,100))
                if(mousePressed[2] and player.gold >= rareP and now -lastPurcahse >buyDelay):
                    player.gold -= rareP
                    purchase.play()
                    lastPurcahse = now
                    if(rareItem in player.inventory.keys()):
                        player.inventory[rareItem] +=1
                    else:
                        player.inventory[rareItem] = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "game"
        window.blit(cursor, mousePos)
        pygame.display.update()
        clock.tick(60)
