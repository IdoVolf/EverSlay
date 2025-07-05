import pygame
pygame.init()

winSize = (640,380)
window = pygame.display.set_mode(winSize)
clock = pygame.time.Clock()
run  = True

while run:

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False


    pygame.display.update()
    clock.tick(60)