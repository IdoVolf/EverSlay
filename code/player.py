import pygame
from reso import resource_path
pygame.init()

weaponToDmg = {"stick":3,"scythe":7,"dagger":16,"annoying dog?":1,"great sword":30,"mace":26,
               "axe":22}
armorToDefense = {"blue shirt":0.1,"baseball hat":0.2,"cupboard":0.3,"crown":0.45,"chestplate":0.55}

slashAnim = [pygame.image.load(resource_path("assets/uniqe/slash1.png")),pygame.image.load(resource_path("assets/uniqe/slash2.png")),
             pygame.image.load(resource_path("assets/uniqe/slash3.png")),pygame.image.load(resource_path("assets/uniqe/slash4.png")),
             pygame.image.load(resource_path("assets/uniqe/slash5.png")),pygame.image.load(resource_path("assets/uniqe/slash6.png")),
             pygame.image.load(resource_path("assets/uniqe/slash7.png")),pygame.image.load(resource_path("assets/uniqe/slash8.png"))]

class Player:
    def __init__(self):
        self.hp = 50
        self.weapon = "scythe"
        self.armor = "blue shirt"
        self.maxHp = 50
        self.monsterKilled = 0
        self.isAttacking = False
        self.attackStart = 0
        self.attackDuration = 800
        self.gold = 50
        self.defenseBoost =1
        self.defBoostTurns =0
        self.inventory = {}


    def getDmg(self):
        return weaponToDmg[self.weapon]
    
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
                img = slashAnim[int(frame)]
                img = pygame.transform.scale(img,(88,88))
                window.blit(img,pos)
            else:
                self.isAttacking = False

    def attackMonster(self, slotStatus, target, slash):
        if slotStatus[target] is not None:
            slash.play()
            self.isAttacking = True
            self.attackStart = pygame.time.get_ticks()
            slotStatus[target].getHit(self.getDmg())
            return target
        return None

    def die(self):
        if(self.hp < 1):
            return "menu"
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