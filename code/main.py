import pygame
from reso import resource_path
from mnst import Monster, loadMonsterAssets, handleMonster, generateRandomMnst, drawIndicator
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

# Target is now the slot index: 0=left, 1=center, 2=right
target = 1

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

# Fixed slots for monsters, always the "source of truth"
monsterSlots = [(260, 148), (50, 148), (450, 148)]  # left(0), center(1), right(2)
slotStatus = [None, None, None]  # holds Monsters or None

slashPoss = [(260,176), (50,176), (450,176)]  # match slot indices order for slash pos
indicPoses = [(260,30), (50,30), (450,30)]    # same here for indicator

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
                if btn.name == "fight":
                    # Attack the monster in the targeted slot, if it exists
                    if slotStatus[target] is not None:
                        slash.play()
                        player.isAttacking = True
                        player.attackStart = pygame.time.get_ticks()
                        slashPosCurrent = target 
                        slotStatus[target].getHit(player.getDmg())
                elif btn.name == "item":
                    turn = "monster"
                elif btn.name == "exit":
                    gameState = "menu"

        # Display monsters and update
        monsters = []  # We'll rebuild this list for convenience (not used for indexing target!)
        for i, mns in enumerate(slotStatus):
            if mns is not None:
                monsters.append(mns)
                displayText(window, f"{mns.hp}", (mns.pos[0] + 40, 120), myFont, (0, 0, 0))
                displayText(window, f"monster defense : {mns.defense}", (mns.pos[0], mns.pos[1] - 50), myFont, (0, 0, 0))
                displayText(window, f"monster attack : {mns.attack}", (mns.pos[0], mns.pos[1] - 70), myFont, (0, 0, 0))
                
                handleMonster(mns, window)

                # Click to change target
                if mns.isClicked(mousePoS, mousePressed) and turn == "player" and not player.isAttacking:
                    target = i  # target is slot index directly
                
                # Check for death
                if mns.hp < 1:
                    slotStatus[i] = None
                    player.monsterKilled += 1
                    turn = "player"
                    killPriority = True
                    
                    # Adjust target if current slot is dead
                    if slotStatus[target] is None:
                        # Pick first alive slot or fallback to 0
                        for j in range(3):
                            if slotStatus[j] is not None:
                                target = j
                                break
                        else:
                            target = 0
                    break

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

        # Update monsters list for convenience after spawning
        monsters = [m for m in slotStatus if m is not None]

        # Fix positions if needed (to avoid overlaps when 1 or 2 monsters present)
        alive_slots = [i for i, m in enumerate(slotStatus) if m is not None]

        if len(alive_slots) == 1:
            i = alive_slots[0]
            if slotStatus[i].pos[0] != monsterSlots[i][0]:
                slotStatus[i].pos = monsterSlots[i]

        elif len(alive_slots) == 2:
            # Make sure monsters occupy different positions, fix if they overlap
            first, second = alive_slots
            if slotStatus[first].pos == slotStatus[second].pos:
                # Push second monster to its correct slot position
                slotStatus[second].pos = monsterSlots[second]

        # Player attack animation
        if player.isAttacking:
            player.drawAnims(window, slashPoss[slashPosCurrent])
            if pygame.time.get_ticks() - player.attackStart >= player.attackDuration:
                player.isAttacking = False
                if not killPriority:
                    turn = "monster"
                    lastTurnTime = pygame.time.get_ticks()
                else:
                    turn = "player"
                    killPriority = False

        # Adjust encounter number by monsters killed
        if player.monsterKilled != 0:
            if player.monsterKilled % 5 == 0:
                encounterNum = 3
            elif player.monsterKilled % 4 == 0:
                encounterNum = 2
            else:
                encounterNum = 1
        else:
            encounterNum = 1

        # Draw indicator on targeted slot (only if that slot is alive)
        if slotStatus[target] is not None:
            lastFrame, frame = drawIndicator(window, indicPoses[target], lastFrame, delay, frame)

        displayText(window, f"Your health : {player.hp}/{player.maxHp} hp", (350, 300), myFont, (0, 0, 0))
        displayText(window, f"Your weapon : {player.weapon} - {player.getDmg()} dmg", (350, 320), myFont, (0, 0, 0))
        displayText(window, f"Your armor : {player.armor} - {player.getDefense()} def", (350, 340), myFont, (0, 0, 0))
        displayText(window, f"Monsters killed : {player.monsterKilled}", (350, 360), myFont, (0, 0, 0))

        window.blit(cursor, mousePoS)
        pygame.display.update()
        clock.tick(60)
