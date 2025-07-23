from item import rare,regularShop,regularBottom
import pygame
from reso import resource_path
from menu import displayText 
import random
pygame.init()
pygame.mixer.init()

def Shop(window, player, rareN):
    # Load assets and setup
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    purchaseSound = pygame.mixer.Sound(resource_path("assets/sound/cash-register-purchase-87313.mp3"))
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    buyDelay = 400
    lastPurchase = 0

    pricesTop = [player.pPrice,player.pPrice,player.pPrice]
    pricesBottom = [100, 125, 150]
    rareItem = rare[rareN]
    rarePrice = 250

    while True:
        now = pygame.time.get_ticks()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()

        # Draw background and gold
        window.blit(bg, bg.get_rect())
        displayText(window, f"Gold: {player.gold}", (20, 10), font, (255, 215, 0))

        # Top row items
        for i, item in enumerate(regularShop):
            x, y = 90 + i * 200, 40
            if item.icon:
                window.blit(pygame.transform.scale(item.icon, (64, 64)), (x, y))
            nameRect = displayText(window, item.name, (x, y + 70), font, (0, 0, 0))
            displayText(window, f"{pricesTop[i]}", (x + 25, y + 90), font, (0, 0, 0))

            if nameRect.collidepoint(mousePos):
                displayText(window, item.description, (110,10), font, (0, 0, 0))
                if mousePressed[2] and player.gold >= pricesTop[i] and now - lastPurchase > buyDelay and len(player.inventory) <6:
                    lastPurchase = now
                    player.gold -= pricesTop[i]
                    purchaseSound.play()
                    player.inventory[item] = player.inventory.get(item, 0) + 1

        # Middle unique item
        ux, uy = 256, 190
        if rareItem.icon:
            window.blit(pygame.transform.scale(rareItem.icon, (64, 64)), (ux, uy - 20))
        rareRect = displayText(window, rareItem.name, (ux, uy - 30), font, (255, 215, 100))
        displayText(window, f"{rarePrice}", (ux, uy + 30), font, (255, 215, 100))

        if rareRect.collidepoint(mousePos):
            displayText(window, rareItem.description, (110,10), font, (255, 215, 100))
            if mousePressed[2] and player.gold >= rarePrice and now - lastPurchase > buyDelay and len(player.inventory) <6:
                lastPurchase = now
                player.gold -= rarePrice
                purchaseSound.play()
                player.inventory[rareItem] = player.inventory.get(rareItem, 0) + 1

        # Bottom row items
        for i, item in enumerate(regularBottom):
            x, y = 90 + i * 200, 270
            if item.icon:
                window.blit(pygame.transform.scale(item.icon, (64, 64)), (x, y))
            nameRect = displayText(window, item.name, (x, y + 70), font, (0, 0, 0))
            displayText(window, f"{pricesBottom[i]}", (x + 25, y + 90), font, (0, 0, 0))

            if nameRect.collidepoint(mousePos):
                displayText(window, item.description, (110,10), font, (0, 0, 0))
                if mousePressed[2] and player.gold >= pricesBottom[i] and now - lastPurchase > buyDelay and len(player.inventory) < 6:
                    lastPurchase = now
                    player.gold -= pricesBottom[i]
                    purchaseSound.play()
                    player.inventory[item] = player.inventory.get(item, 0) + 1

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "game"
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_1):
                    return "game"

        # Cursor and update
        window.blit(cursor, mousePos)
        pygame.display.update()
        clock.tick(60)
