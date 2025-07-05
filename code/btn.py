import pygame

class Button:
    def __init__(self, pos, size, imgDefault, imgHover,name):
        self.pos = pos  # (x, y)
        self.size = size  # (width, height)
        self.imgDefault = pygame.transform.scale(imgDefault,size)
        self.imgHover = pygame.transform.scale(imgHover,size)
        self.rect = pygame.Rect(pos, size)
        self.clicked = False  # tracks click down state
        self.name = name

    def draw(self, window, mousePos):
        if self.rect.collidepoint(mousePos):
            window.blit(self.imgHover, self.pos)
        else:
            window.blit(self.imgDefault, self.pos)

    def isClicked(self, mousePos, mousePressed):
        if self.rect.collidepoint(mousePos):
            if mousePressed[0]:  # left click held
                if not self.clicked:
                    self.clicked = True
                    return True  # click happened
            else:
                self.clicked = False  # reset if released
        else:
            self.clicked = False
        return False
