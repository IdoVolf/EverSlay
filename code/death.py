import pygame
from menu import displayText
from reso import resource_path
pygame.init()


def Death(window,player):
    clock = pygame.time.Clock()
    myFont = pygame.font.Font(None,80)
    cursor = pygame.image.load(resource_path("assets/cursors/crs2.png"))  

    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.fill((0,0,0))
        txt = displayText(window,f"You Died",(250,180),myFont)
        displayText(window,f"You killed {player.monsterKilled}",(250,235),myFont)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "menu"
            
        
        if(txt.collidepoint(mousePos) and mousePressed[0]):
            return "menu"
        
        window.blit(cursor,mousePos)
        pygame.display.update()
        clock.tick(60)
        