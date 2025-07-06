import pygame
from reso import resource_path
pygame.init()

weaponToDmg = {"stick":3,"scythe":7,"poison dagger":11,"quality dagger":18,"annoying dog?":1,"great sword":30,"giant spoon":14,
               "axe":22}
armorToDefense = {"blue shirt":2,"baseball hat":3,"cupboard armor":6,"crown":12,"chestplate":15}

slashAnim = [pygame.image.load(resource_path("assets/uniqe/slash1.png")),pygame.image.load(resource_path("assets/uniqe/slash2.png")),
             pygame.image.load(resource_path("assets/uniqe/slash3.png")),pygame.image.load(resource_path("assets/uniqe/slash4.png")),
             pygame.image.load(resource_path("assets/uniqe/slash5.png")),pygame.image.load(resource_path("assets/uniqe/slash6.png")),
             pygame.image.load(resource_path("assets/uniqe/slash7.png")),pygame.image.load(resource_path("assets/uniqe/slash8.png"))]

class Player:
    def __init__(self):
        self.hp = 50
        self.weapon = "poison dagger"
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
        if(defense < dmg):
            self.hp -= (dmg - defense)
        return
    
    def getDmg(self):
        return weaponToDmg[self.weapon]
    
    def getDefense(self):
        return armorToDefense[self.armor]
    
    def drawAnims(self,window,pos):
        if(self.isAttacking):
            now = pygame.time.get_ticks()
            if(now - self.attackStart < self.attackDuration):
                frame  = (now - self.attackStart) // (self.attackDuration // 8)
                img = slashAnim[int(frame)]
                img = pygame.transform.scale(img,(72,72))
                window.blit(img,pos)
            else:
                self.isAttacking = False