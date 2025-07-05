import pygame
from reso import resource_path
from mnst import Monster
from mnst import loadMonsterAssets
from mnst import handleMonster
from bg import Background
from btn import Button
from menu import menu
from mnst import generateRandomMnst
from menu import displayText

pygame.init()

#stting vars
winSize = (640,380)
window = pygame.display.set_mode(winSize)
clock = pygame.time.Clock()
run  = True
gameState = "menu"
turn = "player"

#loading shit
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))
cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
mnsAssets = loadMonsterAssets(resource_path("assets/mns"))
fight = Button((118,320),(40,40),pygame.image.load(resource_path("assets/btns/fightBtn1.png")),pygame.image.load(resource_path("assets/btns/fightBtn2.png")),"fight")
item = Button((218,320),(40,40),pygame.image.load(resource_path("assets/btns/itemtBtn1.png")),pygame.image.load(resource_path("assets/btns/itemtBtn2.png")),"item")
monsters = []
pygame.mouse.set_visible(False)
btns = [fight]

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

        if(len(monsters) <1):
            newMonst = generateRandomMnst(mnsAssets)
            monsters.append(newMonst)

        for mns in monsters:
            handleMonster(mns,window)

        for btn in btns:
            btn.draw(window,mousePoS)
            if(btn.isClicked(mousePoS,mousePressed)):
                if(btn.name == "fight"):
                    pass
                if(btn.name == "item"):
                    pass

        pygame.display.update() #updating screen each frame
        clock.tick(60)