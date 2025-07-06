import pygame
from item import Item
from reso import resource_path
from menu import displayText 
pygame.init()

def Inventory(window,player):
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    items = player.inventory
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None, 24)

    while(True):
        window.blit(bg,bg.get_rect())

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "game"
            
        count =1
        for i ,j in items.items():
            displayText(window,f"{i.name} - {j}x",(50,50*count),myFont)
            count+=1
        
        pygame.display.update()
        clock.tick(60)



