import pygame
import os
import random
from reso import resource_path
from item import Item
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

    def getHit(self, dmg):
        reduced = int(dmg * self.defense)
        dmg -= reduced
        self.hp -= dmg

        

    def isClicked(self,mousePos,mousePressed):
        img = self.assets[self.currentFrame]    
        img = pygame.transform.scale(img,self.scale)
        rect = img.get_rect(topleft=self.pos)
        return(rect.collidepoint(mousePos) and mousePressed[0])
    


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

monstereastDefs = [0.1,0.15,0.2]
monsterMedDefs = [0.2,0.25,0.3,0.35]
monsterHardDefs = [0.3,0.35,0.4,0.45,0.5,0.55]

def generateRandomMnst(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(5,10),random.randint(4,8),round(random.choice(monstereastDefs),2),(88,88))
    

def generateMedMnst(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(15,30),random.randint(10,15),round(random.choice(monsterMedDefs),2),(88,88))

def generateHardMnst(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(35,55),random.randint(17,25),round(random.choice(monsterHardDefs),2),(88,88))

indic = [pygame.image.load(resource_path("assets/uniqe/indicator/indicator1.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator2.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator3.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator4.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator5.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator6.png")),
         pygame.image.load(resource_path("assets/uniqe/indicator/indicator7.png"))]


def drawIndicator(window, pos, lastFrame, delay, frame):
    now = pygame.time.get_ticks()
    if now - lastFrame > delay:
        frame += 1
        if frame > len(indic) - 1:
            frame = 0
        lastFrame = now
    window.blit(pygame.transform.scale(indic[frame],(48,48)), pos)
    return lastFrame, frame

