import pygame
from reso import resource_path
from mnst import Monster
from mnst import loadMonsterAssets
from mnst import handleMonster
from bg import Background
from btn import Button
from menu import menu

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
fight = Button((118,320),(40,40),pygame.image.load(resource_path("assets/btns/fightBtn1.png")),pygame.image.load(resource_path("assets/btns/fightBtn2.png")),"fight")
monsters = []
pygame.mouse.set_visible(False)
btns = [fight]
gameState = "menu"

while run:
    if(gameState == "menu"):
        gameState,run = menu(window)
    elif(gameState == "game"):

        mousePoS = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.blit(bg,bg.get_rect()) #drawing battle box
        window.blit(cursor,mousePoS)

        for event in pygame.event.get(): #basic event handling
            if(event.type == pygame.QUIT):
                gameState = "menu"

        for mns in monsters:
            handleMonster(mns,window)

        for btn in btns:
            btn.draw(window,mousePoS)
            if(btn.isClicked(mousePoS,mousePressed)):
                if(btn.name == "fight"):
                    print("test")

        pygame.display.update() #updating screen each frame
        clock.tick(60)