import pygame
import os
import random
pygame.init()

class Monster:
    def __init__(self,assets,hp,attack,defense,scale,pos= (260,148)):
        self.assets = assets # a list of pygame images not file paths! (planing to laod the images when game start )
        self.hp =hp
        self.attack = attack
        self.defense = defense
        self.pos = pos
        self.currentFrame = 0
        self.animDelay = 100
        self.lastFrame = 0
        self.scale = scale

    def update(self):
        now = pygame.time.get_ticks()
        if(now - self.lastFrame > self.animDelay):
            self.lastFrame = now
            self.currentFrame +=1
            if(self.currentFrame > len(self.assets)-1):
                self.currentFrame = 0

    def draw(self,window):
        img = self.assets[self.currentFrame]
        img = pygame.transform.scale(img,self.scale)
        window.blit(img,self.pos)

    def getHit(self,dmg):
        if(dmg > self.defense):
            self.hp = self.hp - (dmg-self.defense)
        else:
            self.hp -=1


def loadMonsterAssets(monsterFolderPath):
    allMonsters = []

    for monsterName in os.listdir(monsterFolderPath):
        monsterPath = os.path.join(monsterFolderPath, monsterName)
        if not os.path.isdir(monsterPath):
            continue  # Skip files, only load folders

        frames = []
        for fileName in sorted(os.listdir(monsterPath)):
            if fileName.endswith(".png"):
                imgPath = os.path.join(monsterPath, fileName)
                img = pygame.image.load(imgPath).convert_alpha()
                frames.append(img)
        
        allMonsters.append(frames)

    return allMonsters

def handleMonster(monster,window):
    monster.update()
    monster.draw(window)

def generateRandomMnst(assets):
    newMonst = Monster(assets[random.randint(0,len(assets)-1)],random.randint(5,10),random.randint(4,8),random.randint(3,5),(88,88))
    return newMonst