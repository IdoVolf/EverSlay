import pygame
pygame.init()

class Background:
    def __init__(self,assets):
        self.assets = assets
        self.pos = (35,32)
        self.currentFrame = 0
        self.lastFrame = 0
        self.animeDelay = 100

    def update(self):
        now = pygame.time.get_ticks()
        if(now - self.lastFrame > self.animeDelay):
            self.currentFrame +=1
            self.lastFrame  = now
            if(self.currentFrame > len(self.assets)-1):
                self.currentFrame = 0

    def draw(self,window):
        img = self.assets[self.currentFrame]
        window.blit(img,self.pos)


