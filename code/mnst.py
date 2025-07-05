import pygame
import os
pygame.init()

class Monster:
    def __init__(self,assets,hp,attack,deffence,pos):
        self.assets = assets # a list of pygame images not file paths! (planing to laod the images when game start )
        self.hp =hp
        self.attack = attack
        self.deffence = deffence
        self.pos = pos
        self.currentFrame = 0
        self.animDelay = 100
        self.lastFrame = 0

    def update(self):
        now = pygame.time.get_ticks()
        if(now - self.lastFrame > self.animDelay):
            self.lastFrame = now
            self.currentFrame +=1
            if(self.currentFrame > len(self.assets)-1):
                self.currentFrame = 0

    def draw(self,window):
        img = self.assets[self.currentFrame]
        window.blit(img,self.pos)


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