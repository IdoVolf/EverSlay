import pygame
from reso import resource_path
import random
def changeWeapon(player,weap):
    player.weapon = weap

def changeArmor(player,armor):
    player.armor = armor

def heal(player):
    player.hp += random.randint(15,35)
    if(player.hp > player.maxHp):
        player.hp = player.maxHp

class Item:
    def __init__(self, name, description, icon, effectFunc):
        self.name = name
        self.description = description
        self.icon = icon  # Load an image or None
        self.effectFunc = effectFunc  # Function to call when used

gemI = pygame.image.load(resource_path("assets/items/gem.png"))
healthI = pygame.image.load(resource_path("assets/items/healthP.png"))
axeI = pygame.image.load(resource_path("assets/items/axe.png"))
stickI = pygame.image.load(resource_path("assets/items/stick.png"))
crownI = pygame.image.load(resource_path("assets/items/crown.png"))
trashI = pygame.image.load(resource_path("assets/items/trash1.png"))

gem = Item("Gem","a rare stone worth - 50G",gemI,None)
healthPoition = Item("Health Potion","A poition that heals..",healthI,heal)
trash1 = Item("trash","ewww stop toouching it gross",trashI,None)
axe = Item("axe","an axe used for cutting.. monsters(?)",axeI,changeWeapon)
stick = Item("stick","a small stick",stickI,changeWeapon)
crown = Item("crown","a golden crown!",crownI,changeArmor)

treasures = [gem,healthPoition,axe,stick,crown,trash1,trash1]
equipables = [axe,stick,crown]
