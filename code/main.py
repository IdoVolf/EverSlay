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
from player import Player

pygame.init()
pygame.mixer.init()

#stting vars
winSize = (640,380)
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("EverSlay")
icon = pygame.image.load(resource_path("assets/btns/playBtn1.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
run  = True
gameState = "menu"
turn = "player"
enemyActDelay = 1000  # milliseconds
lastTurnTime = 0
monsters = []
pygame.mouse.set_visible(False)

player = Player()

#loading shit
myFont = pygame.font.Font(None, 24)
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))
cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
mnsAssets = loadMonsterAssets(resource_path("assets/mns"))
exit = Button((20,320),(40,40),pygame.image.load(resource_path("assets/btns/exitBtn1.png")),pygame.image.load(resource_path("assets/btns/exitBtn2.png")),"exit")
fight = Button((118,320),(40,40),pygame.image.load(resource_path("assets/btns/fightBtn1.png")),pygame.image.load(resource_path("assets/btns/fightBtn2.png")),"fight")
item = Button((218,320),(40,40),pygame.image.load(resource_path("assets/btns/itemtBtn1.png")),pygame.image.load(resource_path("assets/btns/itemtBtn2.png")),"item")
btns = [fight,item,exit]
slash = pygame.mixer.Sound(resource_path("assets/sound/slash.mp3"))
bite = pygame.mixer.Sound(resource_path("assets/sound/monster-bite.mp3"))
while run:
    if(gameState == "menu"):
        gameState,run = menu(window)
        player = Player()
        monsters.clear()
    elif(gameState == "game"):
        doorEx = True
        now = pygame.time.get_ticks()
        mousePoS = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.blit(bg,bg.get_rect()) #drawing battle box
        window.blit(cursor,mousePoS)
        
        for event in pygame.event.get(): #basic event handling
            if(event.type == pygame.QUIT):
                gameState = "menu"


        for mns in monsters:
            if(mns.hp < 1):
                monsters.remove(mns)
                player.monsterKilled +=1
            handleMonster(mns,window)
            if(turn == "monster" and now - lastTurnTime > enemyActDelay):
                lastTurnTime =now
                bite.play()
                player.getHit(mns.attack)
                turn = "player"

        if(len(monsters) <1):
            newMonst = generateRandomMnst(mnsAssets)
            monsters.append(newMonst)


        for btn in btns:
            btn.draw(window,mousePoS)
            if(btn.isClicked(mousePoS,mousePressed) and turn == "player" and not player.isAttacking):
                if(btn.name == "fight"):
                    slash.play()
                    player.isAttacking = True
                    player.attackStart = pygame.time.get_ticks()
                    monsters[0].getHit(player.getDmg())
                if(btn.name == "item"):
                    turn = "monster"
                if(btn.name == "exit"):
                    gameState = "menu"
                    



        if player.isAttacking:
           player.drawAnims(window)
           if pygame.time.get_ticks() - player.attackStart >= player.attackDuration:
            player.isAttacking = False
            turn = "monster"
            lastTurnTime = pygame.time.get_ticks()




        displayText(window,f"Your health : {player.hp}/{player.maxHp} hp",(400,300),myFont,(0,0,0))
        displayText(window,f"{monsters[0].hp}",(312,108),myFont,(0,0,0))
        displayText(window,f"monster defense : {monsters[0].defense}",(70,70),myFont,(0,0,0))
        displayText(window,f"monster attack : {monsters[0].attack}",(70,90),myFont,(0,0,0))
        displayText(window,f"Your weapon : {player.weapon} - {player.getDmg()} dmg",(400,320),myFont,(0,0,0))
        displayText(window,f"Your armor : {player.armor} - {player.getDefense()} def",(400,340),myFont,(0,0,0))
        displayText(window,f"Monsters killed : {player.monsterKilled}",(400,360),myFont,(0,0,0))
        pygame.display.update() #updating screen each frame
        clock.tick(60)