import pygame
import os
import random
from reso import resource_path
from item import Item
pygame.init()
pygame.mixer.init()
coinDrop = pygame.mixer.Sound(resource_path("assets/sound/coinDrop.mp3"))

class Monster:
    def __init__(self,assets,hp,attack,defense,scale,type,pos= (260,148)):
        self.assets = assets # a list of pygame images not file paths! (planing to laod the images when game start )
        self.hp =hp
        self.attack = attack
        self.defense = defense
        self.type = type
        self.pos = pos
        self.currentFrame = 0
        self.animDelay = 100
        self.lastFrame = 0
        self.scale = scale
        self.actDelay = 1000

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
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(5,10),random.randint(4,8),round(random.choice(monstereastDefs),2),(88,88),"easy")
    

def generateMedMnst(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(15,30),random.randint(10,15),round(random.choice(monsterMedDefs),2),(88,88),"med")

def generateHardMnst(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.randint(35,55),random.randint(17,25),round(random.choice(monsterHardDefs),2),(88,88),"hard")

def generateBoss(assets):
    return Monster(assets[random.randint(0,len(assets)-1)],random.choice([75,100]),random.choice([20,25,30]),random.choice([0.55,0.45]),(125,125),"BOSS")

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

def scaleDiff(playerMonsteredKilled,scale,hardScale,newKill,rare,rareN,pGold,pGain):
        if(playerMonsteredKilled % 10 == 0 and playerMonsteredKilled != 0 and newKill and scale < 7 and hardScale < 10):
            hardScale +=1
            scale +=1
            newKill = False 
            pGold += pGain
            rareN = random.randint(0,len(rare)-1)
        elif(playerMonsteredKilled % 10 == 0 and newKill and playerMonsteredKilled !=0):
            newKill = False
            pGold += pGain
            rareN = random.randint(0,len(rare)-1)
        return hardScale,scale,newKill,rareN,pGold

def encounterScale(mnsKilled):
    if(mnsKilled % 50 == 0 and (mnsKilled -1) % 50 == 0):
        return 1
    if mnsKilled != 0:
        if mnsKilled % 5 == 0:
                return 3
        elif mnsKilled % 4 == 0:
                return  2
        else:
                return 1
        
    return 1

def spawnLogic(slotStatus, encounterNum, scale, hardScale, mnsAssets, monsterSlots,mnsKilled):
    # Spawn monsters
    bossS = False
    for i in range(len(slotStatus)):
        if slotStatus[i] is None and sum(1 for m in slotStatus if m is not None) < encounterNum:
            isMed = (random.randint(scale, 10) == 10)
            isHard = (random.randint(hardScale, 20)==20)

            if(mnsKilled < 45): 
                if isMed  and mnsKilled >6:
                    newMonst = generateMedMnst(mnsAssets)
                elif isHard and mnsKilled >12:
                    newMonst = generateHardMnst(mnsAssets)
                else:
                    newMonst = generateRandomMnst(mnsAssets)
            else:
                choice = random.choice([1,0,2])
                if(choice == 0):
                    newMonst = generateMedMnst(mnsAssets)
                elif(choice ==1):
                    newMonst = generateHardMnst(mnsAssets)
                else:
                    newMonst = generateRandomMnst(mnsAssets)

            newMonst.pos = monsterSlots[i]
            slotStatus[i] = newMonst
            break
        
    
    # Fix overlapping / positions
    alive_slots = [i for i, m in enumerate(slotStatus) if m is not None]

    if len(alive_slots) == 1:
        i = alive_slots[0]
        if slotStatus[i].pos[0] != monsterSlots[i][0]:
            slotStatus[i].pos = monsterSlots[i]

    elif len(alive_slots) == 2:
        first, second = alive_slots
        if slotStatus[first].pos == slotStatus[second].pos:
            slotStatus[second].pos = monsterSlots[second]

    # Rebuild monsters list
    monsters = [m for m in slotStatus if m is not None]
    return slotStatus, monsters

def monsterAttack(turn, now, lastTurnTime, turnIndex, monsters, bite, player):
    randomN = random.randint(0,15)
    if turn == "monster" and now - lastTurnTime > monsters[0].actDelay:
        if turnIndex < len(monsters):
            lastTurnTime = now
            bite.play()
            player.getHit(monsters[turnIndex].attack)
            if(randomN == 14):
                player.gold -= (player.gold // 3)
                coinDrop.play()
            turnIndex += 1
        else:
            turnIndex = 0
            turn = "player"
    return turn, lastTurnTime, turnIndex, player
