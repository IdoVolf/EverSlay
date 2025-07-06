import pygame
from item import Item
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

    prevRightPressed = False  # Track last frame's right click state

    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        rightPressed = mousePressed[2]  # right mouse button

        window.blit(bg, bg.get_rect())
        window.blit(cursor, mousePos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "game"

        count = 1
        for i in list(items.keys()):
            j = items[i]
            rect = displayText(window, f"{i.name} - {j}x", (50, 50 * count), myFont)
            if rect.collidepoint(mousePos):
                displayText(window, f"{i.description}", (mousePos[0] + 20, mousePos[1] + 20), myFont)

                # Only trigger on the frame the right button was just pressed
                if rightPressed and not prevRightPressed:
                    if i.name == "Health Potion":  # Fix typo if needed
                        player.hp += random.randint(20, 30)
                        items[i] -= 1
                        player.inventory[i] -= 1
                        if items[i] <= 0:
                            del items[i]
                            # No need to del player.inventory[i] separately because both point to same dict

            count += 1

        prevRightPressed = rightPressed  # Update for next frame

        pygame.display.update()
        clock.tick(60)
