import pygame
from btn import Button
from reso import resource_path
from keys import KeyShow
pygame.init()

def menu(window):
    clock = pygame.time.Clock()
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    bg = pygame.image.load(resource_path("assets/menuBg.png"))
    play = Button((290,90),(50,50),pygame.image.load(resource_path("assets/btns/playBtn1.png")),pygame.image.load(resource_path("assets/btns/playBtn2.png")),"play")
    exit = Button((290,250),(50,50),pygame.image.load(resource_path("assets/btns/exitBtn1.png")),pygame.image.load(resource_path("assets/btns/exitBtn2.png")),"exit")
    mouse = Button((290,170),(50,50),pygame.image.load(resource_path("assets/btns/mouse1.png")),pygame.image.load(resource_path("assets/btns/mouse2.png")),"mouse")
    btns = [play,exit,mouse]
    click = pygame.mixer.Sound(resource_path("assets/sound/click.mp3"))

    while True:
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        window.blit(bg,bg.get_rect())
        window.blit(cursor,mousePos)


        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "game",False
            
        for btn in btns:
            btn.draw(window,mousePos)
            if(btn.isClicked(mousePos,mousePressed)):
                click.play()
                if(btn.name == "play"):
                    return "game",True
                elif(btn.name == "exit"):
                    return "game",False
                elif(btn.name == "mouse"):
                    return KeyShow(window)
        
        pygame.display.update()
        clock.tick(60)
        
def displayText(window, text, pos, font, color=(255, 255, 255)):
    txt = font.render(text, True, color)
    rect = txt.get_rect(topleft=pos)
    window.blit(txt, rect)
    return rect
