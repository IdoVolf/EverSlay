import pygame
from reso import resource_path
pygame.init()

#same func here again since circular import and this is the easiet way to fix ;)ss
def displayText1(window, text, pos, font, color=(255, 255, 255)):
    txt = font.render(text, True, color)
    rect = txt.get_rect(topleft=pos)
    window.blit(txt, rect)
    return rect


def KeyShow(window):
    bg = [pygame.image.load(resource_path(f"assets/battle ui/bgs/keys/keyBg{i}.png"))  for i in range(1,6)]
    delay = 100
    currentF = 0
    myFont = pygame.font.Font(None, 24)
    myFontBig = pygame.font.Font(None, 32)
    lastF  =0
    color = (255,255,255)
    cursor = pygame.image.load(resource_path("assets/cursors/crs1.png"))
    clock = pygame.time.Clock()

    while True:
        mousePos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        window.blit(bg[currentF],bg[currentF].get_rect())
        if(now - lastF > delay):
            currentF +=1
            lastF = now
            if(currentF > len(bg)-1):
                currentF = 0
        
        displayText1(window,"Inventory",(50,50),myFontBig,color)
        displayText1(window,"using - right click",(50,80),myFont,color)
        displayText1(window,"selling - middle click",(50,100),myFont,color)

        displayText1(window,"Shop",(50,150),myFontBig,color)
        displayText1(window,"buying - right click",(50,180),myFont,color)

        displayText1(window,"other",(50,230),myFontBig,color)
        displayText1(window,"selecting target - left click",(50,260),myFont,color)
        displayText1(window,"going back - window exit button",(50,280),myFont,color)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "menu",True

        window.blit(cursor,mousePos)        
        pygame.display.update()
        clock.tick(60)

        

