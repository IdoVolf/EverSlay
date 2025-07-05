import pygame
pygame.init()

weaponToDmg = {"stick":3,"rusty knife":7,"short bow":11,"quality dagger":18,"annoying dog?":1,"great Sword":30,"giant spoon":14}
armorToDefense = {"blue shirt":2,"baseball hat":3,"cupboard armor":6,"golden crown":12,"medival armor":15}

class Player:
    def __init__(self):
        self.hp = 50
        self.weapon = "rusty knife"
        self.armor = "blue shirt"
        
    def getHit(self,dmg):
        defense = armorToDefense[self.armor]
        if(defense < dmg):
            self.hp -= (dmg - defense)
        return
    
    def getDmg(self):
        return weaponToDmg[self.weapon]