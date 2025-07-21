import pygame
from reso import resource_path
from buff import Buff
pygame.init()


def goldF(player):
    player.goldGain +=15
    return player

def maxHpF(player):
    player.maxHp +=10
    return player

def cheapPotions(player):
    player.pPrice -= 10
    if(player.pPrice < 25):
        player.pPrice = 35
    return player

def PassiveBuffs(player,window):
    leftPos = (160,150)
    rightPos = (400,150)
    size = (100,100)


    buffsAssets1 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}1.png")) for i in range(1,4)]
    buffsAssets2 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}2.png")) for i in range(1,4)]

    goldB = Buff(leftPos,size,buffsAssets1[0],buffsAssets2[0],"gold",goldF)
    cheaperPotions = Buff(leftPos,size,buffsAssets1[2],buffsAssets2[2],"cheaper potion",cheapPotions)

    maxHpB = Buff(rightPos,size,buffsAssets1[1],buffsAssets2[1],"max hp",maxHpF)

    leftBuffs = [goldB,cheaperPotions]
    rightBuffs = [maxHpB]
