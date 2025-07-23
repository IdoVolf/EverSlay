import pygame
from reso import resource_path
pygame.init()
from death import Death
import random
pygame.mixer.init()
from item import hammer
weaponToDmg = {"stick":3,"scythe":7,"dagger":16,"hammer":35,"bomb":40,"mace":30,
               "axe":22,"frying pan":3,"wand":25}
armorToDefense = {"blue shirt":0.1,"medi bag":0.35,"cupboard":0.3,"crown":0.45,"chestplate":0.55,"glasses":0.2}

slashAnim = [pygame.image.load(resource_path("assets/uniqe/slash1.png")),pygame.image.load(resource_path("assets/uniqe/slash2.png")),
             pygame.image.load(resource_path("assets/uniqe/slash3.png")),pygame.image.load(resource_path("assets/uniqe/slash4.png")),
             pygame.image.load(resource_path("assets/uniqe/slash5.png")),pygame.image.load(resource_path("assets/uniqe/slash6.png")),
             pygame.image.load(resource_path("assets/uniqe/slash7.png")),pygame.image.load(resource_path("assets/uniqe/slash8.png"))]
crit = pygame.mixer.Sound(resource_path("assets/sound/crit.mp3"))
exxplode = pygame.mixer.Sound(resource_path("assets/sound/bomb.mp3"))
bombAnim = [pygame.image.load(resource_path(f"assets/uniqe/bomb/exp{i}.png")) for i in range(1,9)]
class Player:
    def __init__(self):
        self.hp = 50
        self.weapon = "scythe"
        self.armor = "blue shirt"
        self.maxHp = 50
        self.baseMaxHp =50
        self.monsterKilled = 0
        self.isAttacking = False
        self.attackStart = 0
        self.attackDuration = 800
        self.gold = 100
        self.defenseBoost =1
        self.defBoostTurns =0
        self.attackBoost = 1
        self.attackBoostTurns = 0
        self.bombTurns = 0
        self.goldGain = 50
        self.pPrice = 75
        self.vamp = 0
        self.armHpB = 0
        self.battleAnim = slashAnim
        self.xp =0
        self.crit = 3 #%
        self.inventory = {}


    def getDmg(self):
        return round(weaponToDmg[self.weapon] * self.attackBoost)
    
    def getDefense(self):
        return round(armorToDefense[self.armor]*self.defenseBoost,2)
    
    def getHit(self,dmg):
        defense = self.getDefense()
        dmg -= int(dmg * defense)
        self.hp -= dmg
    
    
    def drawAnims(self,window,pos):
        if(self.isAttacking):
            now = pygame.time.get_ticks()
            if(now - self.attackStart < self.attackDuration):
                frame  = (now - self.attackStart) // (self.attackDuration // 8)
                img = self.battleAnim[int(frame)]
                img = pygame.transform.scale(img,(88,88))
                window.blit(img,pos)
            else:
                self.isAttacking = False

    def attackMonster(self, slotStatus, target, slash):
        if slotStatus[target] is not None:
            dmg = self.getDmg()
            if((random.randint(self.crit,100) == 100) or (self.weapon == "frying pan" and (random.choice([0,1])==1))):
                if(self.weapon == "frying pan"):
                    exxplode.play()
                    self.weapon = "scythe"
                dmg = 9999
                crit.play()
            if(self.weapon != "bomb" and self.weapon != "wand"):
                slash.play()
                self.battleAnim = slashAnim
                if(self.weapon == "hammer"):
                    choice = (random.randint(1,10) == 9)
                    if(choice):
                        exxplode.play()
                        self.weapon = "dagger"
            else:
                self.battleAnim = bombAnim
                exxplode.play()
            self.hp += self.vamp
            if(self.hp > self.maxHp):
                self.hp = self.maxHp
            self.isAttacking = True
            self.attackStart = pygame.time.get_ticks()
            slotStatus[target].getHit(dmg)
            return target
        return None

    def die(self,window):
        if(self.hp < 1):
            return Death(window,self)
        return "game"
    
    def slashAnim(self,window,slashPoss,slashPosCurrent,lastTurnTime,turn,killPriority):
        if self.isAttacking:
            self.drawAnims(window, slashPoss[slashPosCurrent])
            if pygame.time.get_ticks() - self.attackStart >= self.attackDuration:
                self.isAttacking = False
                if not killPriority:
                    turn = "monster"
                    lastTurnTime = pygame.time.get_ticks()
                else:
                    turn = "player"
                    killPriority = False
        return turn,lastTurnTime,killPriority