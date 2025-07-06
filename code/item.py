import pygame
from reso import resource_path
class Item:
    def __init__(self, name, description, icon, effectFunc):
        self.name = name
        self.description = description
        self.icon = icon  # Load an image or None
        self.effectFunc = effectFunc  # Function to call when used

gemI = pygame.image.load(resource_path("assets/items/gem.png"))
healthI = pygame.image.load(resource_path("assets/items/healthP.png"))
gem = Item("Gem","a rare stone worth - 50G",gemI,None)
healthPoition = Item("Health Potion","A poition that heals..",healthI,None)
treasures = [gem,healthPoition]