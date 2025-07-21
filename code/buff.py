import pygame
from reso import resource_path
pygame.init()

class Buff:
    def __init__(self, pos, size, imgDefault, imgHover,name,effectFunc):
        self.pos = pos  
        self.size = size  
        self.imgDefault = pygame.transform.scale(imgDefault,size)
        self.imgHover = pygame.transform.scale(imgHover,size)
        self.effectFunc = effectFunc
        self.rect = pygame.Rect(pos, size)
        self.clicked = False  
        self.name = name

    def draw(self, window, mousePos):
        if self.rect.collidepoint(mousePos):
            window.blit(self.imgHover, self.pos)
        else:
            window.blit(self.imgDefault, self.pos)

    def isClicked(self, mousePos, mousePressed,player):
        if self.rect.collidepoint(mousePos):
            if mousePressed[0]:  # left click held
                if not self.clicked:
                    self.clicked = True
                    player = self.effectFunc(player)

    
    def isHovered(self,mousePos):
        return self.rect.collidepoint(mousePos)

leftPos = (160,150)
rightPos = (400,150)
size = (100,100)

buffsAssets1 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}1.png")) for i in range(1,4)]
buffsAssets2 = [pygame.image.load(resource_path(f"assets/buffs/buff{i}2.png")) for i in range(1,4)]
goldB = Buff(leftPos,)