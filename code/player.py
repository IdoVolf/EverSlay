import pygame
from reso import resource_path
pygame.init()

weaponToDmg = {"stick":3,"scythe":7,"poison dagger":11,"quality dagger":18,"annoying dog?":1,"great sword":30,"giant spoon":14,
               "axe":22}
armorToDefense = {"blue shirt":0.1,"baseball hat":0.2,"cupboard armor":0.3,"crown":0.45,"chestplate":0.55}

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
        self.gold = 0
        self.inventory = {}

    def getHit(self,dmg):
        defense = armorToDefense[self.armor]
        dmg -= int(dmg * defense)
        self.hp -= dmg
    
    def getDmg(self):
        return weaponToDmg[self.weapon]
    
    def getDefense(self):
        return round(armorToDefense[self.armor],2)
    
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