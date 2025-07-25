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

def addDefenseBoost(player):
    player.defenseBoost = 1.5
    player.defBoostTurns =1

def addDmg(player):
        player.attackBoost = 1.5
        player.attackBoostTurns = 1

def Bomb(player):
    player.weapon = "bomb"
    player.bombTurns =3

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
maceI = pygame.image.load(resource_path("assets/items/mace.png"))
defensePI = pygame.image.load(resource_path("assets/items/defenseP.png"))
attackPI = pygame.image.load(resource_path("assets/items/attackPotion.png"))
bombI = pygame.image.load(resource_path("assets/items/bomb.png"))
mediI = pygame.image.load(resource_path("assets/items/mediBag.png"))
panI = pygame.image.load(resource_path("assets/items/pan.png"))
wandI = pygame.image.load(resource_path("assets/items/wand.png"))
glassesI = pygame.image.load(resource_path("assets/items/glasses.png"))
hammerI = pygame.image.load(resource_path("assets/items/hammer.png"))

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
mace = Item("mace","a stick with pointy metal ball on top",maceI,changeWeapon)
defenseP = Item("Defense potion","gives you defense",defensePI,addDefenseBoost)
attackP = Item("attack potion","give you attack bonous for 1 attack",attackPI,addDmg)
bomb = Item("bomb","a bomb can be used 3 times after destroyed becomes a sycthe..",bombI,Bomb)
mediBag = Item("medi bag","low defense more max hp..",mediI,changeArmor)
pan = Item("frying pan","a huge crit chance somehow.. if crit turn to scythe",panI,changeWeapon)
wand = Item("wand","a magic wand rare loot",wandI,changeWeapon)
glasses = Item("glasses","sun glasses used for blocking the sun and (monsters?)",glassesI,changeArmor)
hammer = Item("hammer","a big hammer a hit might break it and turn it to a dagger",hammerI,changeWeapon)

treasures = [gem,gem,gem,healthPoition,stick,trash1,hammer,trash1,scythe,glasses,glasses,cupboard,dagger,defenseP,attackP,bomb,gem,trash1,gem,gem,pan,dagger,trash1,wand,gem,stick]
equipables = [axe,stick,crown,scythe,chestplate,cupboard,dagger,mace,bomb,mediBag,pan,wand,glasses,hammer]
regularShop = [healthPoition,attackP,defenseP]
regularBottom = [cupboard,dagger,crown]
rare = [axe,chestplate,mace,bomb,mediBag,pan,hammer,axe,bomb]
g30Sell = [dagger,crown,axe,defenseP,healthPoition,attackP,chestplate,bomb,mediBag,pan,wand,hammer]
g10Sell = [trash1,stick,cupboard,scythe,glasses]
