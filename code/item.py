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

def sell(player,price):
    player.gold += price

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
scytheI = pygame.image.load(resource_path("assets/items/scythe.png"))
chestplateI = pygame.image.load(resource_path("assets/items/chestplate.png"))
cupboardI =  pygame.image.load(resource_path("assets/items/cupboard.png"))
daggerI = pygame.image.load(resource_path("assets/items/dagger.png"))

gem = Item("Gem","a rare stone worth - 50G",gemI,sell)
healthPoition = Item("Health Potion","A poition that heals..",healthI,heal)
trash1 = Item("trash","ewww stop toouching it gross",trashI,None)
axe = Item("axe","an axe used for cutting.. monsters(?)",axeI,changeWeapon)
stick = Item("stick","a small stick",stickI,changeWeapon)
crown = Item("crown","a golden crown!",crownI,changeArmor)
scythe = Item("scythe","an ugly looking scythe",scytheI,changeWeapon)
chestplate = Item("chestplate","a shiny mettalic chestplate",chestplateI,changeArmor)
cupboard = Item("cupboard","an armor made out of cupboard",cupboardI,changeArmor)
dagger = Item("dagger","a dagger...",daggerI,changeWeapon)

treasures = [gem,gem,gem,healthPoition,axe,stick,crown,trash1,trash1,scythe,chestplate,cupboard,dagger]
equipables = [axe,stick,crown,scythe,chestplate,cupboard,dagger]
regularShop = [healthPoition,crown,dagger]