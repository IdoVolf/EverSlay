import pygame
from item import Item ,equipables,g10Sell,g30Sell
from reso import resource_path
from menu import displayText 
import random
pygame.init()
pygame.mixer.init()

def Inventory(window, player):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    items = player.inventory
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    drink = pygame.mixer.Sound(resource_path("assets/sound/drinking-coffe-107121.mp3"))

    delay = 5000  # 5 seconds per item
    if not hasattr(player, "lastUseTime"):
        player.lastUseTime = {}

    prevMidPressed = False  # <- Track previous middle click
    prevRightPressed = False

    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        rightPressed = mousePressed[2]  # right mouse button
        midPressed = mousePressed[1]    # middle mouse button
        now = pygame.time.get_ticks()

        window.blit(bg, bg.get_rect())
        window.blit(cursor, mousePos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "game"

        count = 1
        for i in list(items.keys()):
            j = items[i]
            rect = displayText(window, f"{i.name} - {j}x", (50, 50 * count), myFont)
            window.blit(pygame.transform.scale(i.icon, (48, 48)), (200, (50 * count)-10))

            if i not in player.lastUseTime:
                player.lastUseTime[i] = 0

            if rect.collidepoint(mousePos):
                displayText(window, f"{i.description}", (mousePos[0] + 20, mousePos[1] + 20), myFont)

                if rightPressed and not prevRightPressed and now - player.lastUseTime[i] > delay:
                    player.lastUseTime[i] = now
                    if i.name == "Health Potion":
                        drink.play()
                        i.effectFunc(player)
                        items[i] -= 1
                        if items[i] <= 0:
                            del items[i]
                            del player.lastUseTime[i]
                    elif i.name == "Gem":
                        i.effectFunc(player,50)
                        items[i] -=1
                        if(items[i] <=0):
                            del items[i]
                            del player.lastUseTime[i]
                    elif i.name == "Defense potion":
                        drink.play()
                        i.effectFunc(player)
                        items[i] -=1
                        if(items[i] <=0):
                            del items[i]
                            del player.lastUseTime[i]
                    elif i.name == "attack potion":
                        drink.play()
                        i.effectFunc(player)
                        items[i] -=1
                        if(items[i] <=0):
                            del items[i]
                            del player.lastUseTime[i]
                    elif i.name == "ladder":
                        slotStatus, encounterNumber = i.effectFunc(slotStatus,encounterNumber)
                        items[i] -=1
                        if(items[i] <= 0):
                            del items[i]
                            del player.lastUseTime[i]
                    elif i in equipables:
                        if(i.name != "bomb"):
                            i.effectFunc(player, i.name)
                        else:
                            i.effectFunc(player)
                        items[i] -= 1
                        if items[i] <= 0:
                            del items[i]
                            del player.lastUseTime[i]

                elif midPressed and not prevMidPressed and now - player.lastUseTime[i] > delay:
                    items[i] -=1
                    player.lastUseTime[i] = now
                    if(i in g10Sell):
                        player.gold +=10
                    elif(i in g30Sell):
                        player.gold += 30
                    if(items[i] <=0):
                        del items[i]
                        del player.lastUseTime[i]

            count += 1

        prevRightPressed = rightPressed
        prevMidPressed = midPressed  # <- Update previous state

        pygame.display.update()
        clock.tick(60)
