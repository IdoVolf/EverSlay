import pygame
from item import Item ,equipables
from reso import resource_path
from menu import displayText 
import random
pygame.init()



import pygame
from item import Item, equipables
from reso import resource_path
from menu import displayText 
import random
pygame.init()

def Inventory(window, player):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    items = player.inventory
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))

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
                    elif i in equipables:
                        i.effectFunc(player, i.name)
                        items[i] -= 1
                        if items[i] <= 0:
                            del items[i]
                            del player.lastUseTime[i]

                elif midPressed and not prevMidPressed and now - player.lastUseTime[i] > delay:
                    player.lastUseTime[i] = now
                    del items[i]
                    del player.lastUseTime[i]

            count += 1

        prevRightPressed = rightPressed
        prevMidPressed = midPressed  # <- Update previous state

        pygame.display.update()
        clock.tick(60)
