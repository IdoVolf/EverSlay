import pygame
from reso import resource_path
pygame.init()

class Buff:
    def __init__(self, pos, size, imgDefault, imgHover, name, effectFunc):
        self.pos = pos  
        self.size = size  
        self.imgDefault = pygame.transform.scale(imgDefault, size)
        self.imgHover = pygame.transform.scale(imgHover, size)
        self.effectFunc = effectFunc
        self.rect = pygame.Rect(pos, size)
        self.clicked = False  
        self.name = name

    def draw(self, window, mousePos):
        if self.rect.collidepoint(mousePos):
            window.blit(self.imgHover, self.pos)
        else:
            window.blit(self.imgDefault, self.pos)

    def isClicked(self, mousePos, mousePressed, player):
        if self.rect.collidepoint(mousePos):
            if mousePressed[0] and not self.clicked:
                self.clicked = True
                player = self.effectFunc(player)
                return player, True
        else:
            self.clicked = False
        return player, False

    def isHovered(self, mousePos):
        return self.rect.collidepoint(mousePos)

    def update(self, mousePressed):
        if not mousePressed[0]:
            self.clicked = False
