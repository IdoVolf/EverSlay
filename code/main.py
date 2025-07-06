import pygame
from reso import resource_path
from mnst import Monster, loadMonsterAssets, handleMonster, generateRandomMnst,drawIndicator
from bg import Background
from btn import Button
from menu import menu, displayText
from player import Player

pygame.init()
pygame.mixer.init()

winSize = (640, 380)
window = pygame.display.set_mode(winSize)
pygame.display.set_caption("EverSlay")
icon = pygame.image.load(resource_path("assets/btns/playBtn1.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
run = True
gameState = "menu"
turn = "player"
enemyActDelay = 1000
lastTurnTime = 0
monsters = []
pygame.mouse.set_visible(False)
player = Player()
killPriority = False
target =1
delay = 100
lastFrame = 0
frame = 0

myFont = pygame.font.Font(None, 24)
bg = pygame.image.load(resource_path("assets/battle ui/battleBox.png"))
cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
mnsAssets = loadMonsterAssets(resource_path("assets/mns"))

exit = Button((20, 320), (40, 40),
              pygame.image.load(resource_path("assets/btns/exitBtn1.png")),
              pygame.image.load(resource_path("assets/btns/exitBtn2.png")), "exit")
fight = Button((118, 320), (40, 40),
               pygame.image.load(resource_path("assets/btns/fightBtn1.png")),
               pygame.image.load(resource_path("assets/btns/fightBtn2.png")), "fight")
item = Button((218, 320), (40, 40),
              pygame.image.load(resource_path("assets/btns/itemtBtn1.png")),
              pygame.image.load(resource_path("assets/btns/itemtBtn2.png")), "item")
btns = [fight, item, exit]

slash = pygame.mixer.Sound(resource_path("assets/sound/slash.mp3"))
bite = pygame.mixer.Sound(resource_path("assets/sound/monster-bite.mp3"))

encounterNum = 1
turnIndex = 0
monsterSlots = [(260, 148), (50, 148), (450, 148)]  # slots: left(0), center(1), right(2)
slotStatus = [None, None, None]  # holds Monsters or None
slashPoss = [(50,176),(282, 176),(450,176)]
indicPoses = [(55,30),(282,30),(450,30)]

while run:
    if gameState == "menu":
        gameState, run = menu(window)
        player = Player()
        monsters.clear()
        encounterNum = 1
        slotStatus = [None, None, None]
        turn = "player"
        killPriority = False
        turnIndex = 0

    elif gameState == "game":
        now = pygame.time.get_ticks()
        mousePoS = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()

        window.blit(bg, bg.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "menu"


        for btn in btns:
            btn.draw(window, mousePoS)
            if btn.isClicked(mousePoS, mousePressed) and turn == "player" and not player.isAttacking:
                if btn.name == "fight" and monsters:
                    slash.play()
                    player.isAttacking = True
                    player.attackStart = pygame.time.get_ticks()
                    monsters[target].getHit(player.getDmg())  # always attack center monster
                if btn.name == "item":
                    turn = "monster"
                if btn.name == "exit":
                    gameState = "menu"

        # Display monsters and update
        for mns in monsters:
            displayText(window, f"{mns.hp}", (mns.pos[0] + 40, 120), myFont, (0, 0, 0))
            displayText(window, f"monster defense : {mns.defense}", (mns.pos[0], mns.pos[1] - 50), myFont, (0, 0, 0))
            displayText(window, f"monster attack : {mns.attack}", (mns.pos[0], mns.pos[1] - 70), myFont, (0, 0, 0))
            if(mns.isClicked(mousePoS,mousePressed)):
                target = monsters.index(mns)
            if mns.hp < 1:
                deadIndex = slotStatus.index(mns)
                slotStatus[deadIndex] = None
                monsters.remove(mns)
                player.monsterKilled += 1
                turn = "player"
                killPriority = True
                break

            handleMonster(mns, window)

        # Monster attack turn logic
        if turn == "monster" and now - lastTurnTime > enemyActDelay:
            if turnIndex < len(monsters):
                lastTurnTime = now
                bite.play()
                player.getHit(monsters[turnIndex].attack)
                turnIndex += 1
            else:
                turnIndex = 0
                turn = "player"

        # Spawn monsters in empty slots
        for i in range(len(slotStatus)):
            if slotStatus[i] is None and len(monsters) < encounterNum:
                newMonst = generateRandomMnst(mnsAssets)
                newMonst.pos = monsterSlots[i]
                slotStatus[i] = newMonst
                break

        # Rebuild monster list: center (slot 1) first, then left (0), then right (2)
        monsters = [slotStatus[1], slotStatus[0], slotStatus[2]]
        monsters = [m for m in monsters if m is not None]

        if(len(monsters) ==1):
            if(monsters[0].pos[0] != 260):
                monsters[0].pos = (260,148)
            target =0

        if(len(monsters) == 2):
            if(monsters[1].pos[0] == 450):
                monsters[1].pos = (260,148)
            if(target == 2):
                target =0
            
            if(monsters[1].pos == monsters[0].pos):
                monsters[1].pos = (50,148)

        # Player attack animation
        if player.isAttacking:
            if(len(monsters)>1):
                player.drawAnims(window,slashPoss[target])
            else:
                player.drawAnims(window,slashPoss[target+1])
            if pygame.time.get_ticks() - player.attackStart >= player.attackDuration:
                player.isAttacking = False
                if not killPriority:
                    turn = "monster"
                    lastTurnTime = pygame.time.get_ticks()
                else:
                    turn = "player"
                    killPriority = False

        if(player.monsterKilled %5==0 and player.monsterKilled != 0):
            encounterNum = 3
        elif(player.monsterKilled % 4 ==0) and player.monsterKilled != 0:
            encounterNum =2
        else:
            encounterNum =1

        # HUD
        if(len(monsters)>1):
            lastFrame, frame = drawIndicator(window, indicPoses[target], lastFrame, delay, frame)
        else:
            lastFrame, frame = drawIndicator(window, indicPoses[target+1], lastFrame, delay, frame)
        displayText(window, f"Your health : {player.hp}/{player.maxHp} hp", (350, 300), myFont, (0, 0, 0))
        displayText(window, f"Your weapon : {player.weapon} - {player.getDmg()} dmg", (350, 320), myFont, (0, 0, 0))
        displayText(window, f"Your armor : {player.armor} - {player.getDefense()} def", (350, 340), myFont, (0, 0, 0))
        displayText(window, f"Monsters killed : {player.monsterKilled}", (350, 360), myFont, (0, 0, 0))
        window.blit(cursor, mousePoS)
        pygame.display.update()
        clock.tick(60)
