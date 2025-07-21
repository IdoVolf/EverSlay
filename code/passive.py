import pygame
from reso import resource_path
import random
from buff import Buff
pygame.init()

def goldF(player):
    player.goldGain +=15
    return player

def maxHpF(player):
    player.baseMaxHp += 5
    return player

def cheapPotions(player):
    player.pPrice -= 10
    if(player.pPrice < 35):
        player.pPrice = 35
    return player

def vampF(player):
    player.vamp +=2
    return player

def critF(player):
    player.crit += 2
    return player

def PassiveBuffs(player,window):
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    bg = pygame.image.load(resource_path("assets/battle ui/bgs/inventory.png"))
    click = pygame.mixer.Sound(resource_path("assets/sound/click.mp3"))
    clock = pygame.time.Clock()

    leftPos = (160,150)
    rightPos = (400,150)
    size = (100,100)

    buffsAssets1 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}1.png")) for i in range(1,6)]
    buffsAssets2 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}2.png")) for i in range(1,6)]

    goldB = Buff(leftPos,size,buffsAssets1[0],buffsAssets2[0],"gold",goldF)
    cheaperPotions = Buff(leftPos,size,buffsAssets1[2],buffsAssets2[2],"cheaper potion",cheapPotions)
    critB = Buff(leftPos,size,buffsAssets1[4],buffsAssets2[4],"better crit chance",critF)

    maxHpB = Buff(rightPos,size,buffsAssets1[1],buffsAssets2[1],"max hp",maxHpF)
    vampB = Buff(rightPos,size,buffsAssets1[3],buffsAssets2[3],"vampire steal hp",vampF)

    leftBuffs = [goldB,cheaperPotions,critB]
    rightBuffs = [maxHpB,vampB]

    rightBuff = random.choice(rightBuffs)
    leftBuff = random.choice(leftBuffs)
    buffs = [rightBuff,leftBuff]
    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.blit(bg,bg.get_rect())

        for buff in buffs:
            buff.draw(window,mousePos)
            buff.update(mousePressed)
            player,clicked = buff.isClicked(mousePos,mousePressed,player)
            if(clicked):
                return "game",player
            
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "game",player


        window.blit(cursor,mousePos)
        pygame.display.update()
        clock.tick(60)
