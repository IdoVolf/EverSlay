import pygame
from reso import resource_path
from mnst import Monster, loadMonsterAssets, handleMonster, generateRandomMnst,generateMedMnst,generateHardMnst,drawIndicator,scaleDiff,encounterScale,spawnLogic,monsterAttack
from bg import Background
from btn import Button
from menu import menu, displayText
from player import Player
from inventory import Inventory
from item import treasures ,rare
import random
from shop import Shop
from displayInfo import displayPlayerInfo ,displayMonsterInfo
from passive import PassiveBuffs
pygame.init()
pygame.mixer.init()
turnChanged = True

winSize = (640, 380)
flags = pygame.RESIZABLE
window = pygame.display.set_mode(winSize, flags)

fullscreen = False

display_info = pygame.display.Info()
fullscreen_size = (display_info.current_w, display_info.current_h)

icon = pygame.image.load(resource_path("assets/btns/playBtn1.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
run = True
gameState = "menu"
turn = "player"
lastTurnTime = 0
monsters = []
pygame.mouse.set_visible(False)
player = Player()
killPriority = False
# Target is now the slot index: 0=left, 1=center, 2=right
target = 1
pygame.display.set_caption("EverSlay")
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
shop = Button((270,320),(40,40),
              pygame.image.load(resource_path("assets/btns/shopBtn1.png")),
              pygame.image.load(resource_path("assets/btns/shopBtn2.png")),"shop")
btns = [fight, item, exit,shop]

slash = pygame.mixer.Sound(resource_path("assets/sound/slash.mp3"))
bite = pygame.mixer.Sound(resource_path("assets/sound/monster-bite.mp3"))
treasureSe = pygame.mixer.Sound(resource_path("assets/sound/arcade-ui-14-229514.mp3"))
die = pygame.mixer.Sound(resource_path("assets/sound/pick-92276.mp3"))
click = pygame.mixer.Sound(resource_path("assets/sound/click.mp3"))

encounterNum = 1
turnIndex = 0

# Fixed slots for monsters, always the "source of truth"
monsterSlots = [(260, 148), (50, 148), (450, 148)]  # left(0), center(1), right(2)
slotStatus = [None, None, None]  # holds Monsters or None
slashPosCurrent = 0
slashPoss = [(260,176), (50,176), (450,176)]  # match slot indices order for slash pos
indicPoses = [(280,30), (70,30), (470,30)]    # same here for indicator
scale = 0
hardScale = 0
newKill = True
rareN = random.randint(0,len(rare)-1)
defBoostActive = False
dif = ["easy","med","hard","BOSS"]
xps = [1,2,3,10]
requiredXp = 10
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
        target = 1  # always start targeting center slot
        scale = 0
        hardScale = 0
        newKill = True
        rareN = random.randint(0,len(rare)-1)
        requiredXp  = 10
    elif gameState == "game":
        now = pygame.time.get_ticks()
        mousePoS = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.blit(bg, bg.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:  # Your toggle key
                    fullscreen = not fullscreen
                    if fullscreen:
                        # Go fullscreen at native desktop resolution
                        window = pygame.display.set_mode(fullscreen_size, pygame.FULLSCREEN)
                    else:
                        # Back to windowed resizable with your original size
                        window = pygame.display.set_mode(winSize, pygame.RESIZABLE)

        gameState = player.die(window)
        for btn in btns:
            btn.draw(window, mousePoS)
            if btn.isClicked(mousePoS, mousePressed) and turn == "player" and not player.isAttacking:
                click.play()
                if btn.name == "fight":
                    pos = player.attackMonster(slotStatus, target, slash)
                    if pos is not None:
                        slashPosCurrent = pos
                elif btn.name == "item":
                    gameState= Inventory(window,player)
                elif btn.name == "exit":
                    gameState = "menu"
                elif btn.name == "shop":
                    gameState = Shop(window,player,rareN)
            elif(btn.isHovered(mousePoS)):
                if(btn.name == "exit"):
                    target =2
                    displayText(window,"WARNING EXITING WILL NOT SAVE YOUR RUN!",(50,60),myFont,(0,0,0))

        # Display monsters and update
        monsters = []  # We'll rebuild this list for convenience (not used for indexing target!)

        for i, mns in enumerate(slotStatus):
            if mns is not None:
                monsters.append(mns)
                displayMonsterInfo(window,mns)
                handleMonster(mns, window)
                if mns.isClicked(mousePoS, mousePressed) and turn == "player" and not player.isAttacking:
                    target = i  

                if mns.hp < 1:
                    player.xp += xps[dif.index(mns.type)]
                    die.play()
                    if(not newKill):
                        newKill = True
                    trs = random.randint(0,len(treasures)-1)
                    if(bool(random.choice([0,0,1]) ==1)):
                        if(len(player.inventory) < 7): 
                            treasureSe.play()
                            if(treasures[trs] in player.inventory):
                                player.inventory[treasures[trs]] = player.inventory[treasures[trs]] +1
                            else:
                                player.inventory[treasures[trs]] = 1
                        else:
                            if(treasures[trs] in player.inventory):
                                player.inventory[treasures[trs]] = player.inventory[treasures[trs]] +1
                                treasureSe.play()
                                
                    slotStatus[i] = None
                    player.monsterKilled += 1
                    turn = "player"
                    killPriority = True
                    turnChanged = True
            
                    if slotStatus[target] is None:
                        # Pick first alive slot or fallback to 0
                        for j in range(3):
                            if slotStatus[j] is not None:
                                target = j
                                break
                        else:
                            target = 0
                    break
        if(turn == "monster" and not player.isAttacking):
            turnChanged = True

        # Monster attack turn logic
        # Spawn monsters in empty slots
        slotStatus, monsters = spawnLogic(slotStatus, encounterNum, scale, hardScale, mnsAssets, monsterSlots,player.monsterKilled)
        # Player attack animation
        turn,lastTurnTime,killPriority = player.slashAnim(window,slashPoss,slashPosCurrent,lastTurnTime,turn,killPriority)
        # Adjust encounter number by monsters killed
        encounterNum = encounterScale(player.monsterKilled)
        #diff scale
        hardScale,scale,newKill,rareN,player.gold= scaleDiff(player.monsterKilled,scale,hardScale,newKill,rare,rareN,player.gold,player.goldGain)
        turn, lastTurnTime, turnIndex, player = monsterAttack(turn, now, lastTurnTime, turnIndex, monsters, bite, player)
        # Only reduce defense boost during monster turn

        if turn == "player" and turnChanged:
            if player.defBoostTurns > 0:
                player.defBoostTurns -= 1
            if player.defBoostTurns == 0:
                player.defenseBoost = 1.0

            if player.attackBoostTurns > 0:
                player.attackBoostTurns -= 1
            if player.attackBoostTurns == 0:
                player.attackBoost = 1.0

            if player.weapon == "bomb":
                player.bombTurns -= 1
                if player.bombTurns == 0:
                    player.weapon = "scythe"

            turnChanged = False  


        # Draw indicator on targeted slot (only if that slot is alive)
        if slotStatus[target] is not None:
            lastFrame, frame = drawIndicator(window, indicPoses[target], lastFrame, delay, frame)

        if(player.armor == "medi bag"):
            player.armHpB = 20
        else:
            player.armHpB = 0

        if(player.xp >= requiredXp):
            player.xp = 0
            requiredXp = round(requiredXp * 1.15)
            gameState,player = PassiveBuffs(player,window)
        
        player.maxHp = player.baseMaxHp + player.armHpB
        displayPlayerInfo(window,player)
        window.blit(cursor, mousePoS)
        pygame.display.update()
        clock.tick(60)
