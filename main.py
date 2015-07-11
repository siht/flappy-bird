import pygame, sys
from pygame.locals import *
from graphics import Bird, BackGround, Pipe, PipeInverted, Floor, Logo
from preferences import *

class Helper(object):
    i = FLOOR_TIME
    @staticmethod
    def add_floor(group, obj):
        if Helper.i == FLOOR_TIME:
            Helper.i = 0
            group.add(obj)
        Helper.i += 1

def main():
    pygame.init()
    ventana = pygame.display.set_mode(WINDOW_SIZE, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption('Flappy Bird')
    all = pygame.sprite.RenderUpdates()
    pipes = pygame.sprite.RenderUpdates()
    reloj = pygame.time.Clock()
    dirty_rects = None

    # sprite statics
    background = pygame.Surface(ventana.get_size())
    fondo = BackGround()
    logo = Logo((200, 200))
    tubo = Pipe((100, 400))
    tubo_i = PipeInverted((100, 0))
    # generate the background
    background.blit(fondo.image, fondo.rect)
    # draw the background
    ventana.blit(fondo.image, fondo.rect)
    ventana.blit(logo.image, logo.rect)
    pygame.display.flip()
    # sprite animated
    ave = Bird((105, 330))
    all.add(ave)
    pipes.add(tubo, tubo_i)
    # initialize floor
    for i in range(0, 16):
        all.add(Floor((WINDOW_SIZE[0] - 25*i, 500)))
    keep = True
    while keep:
        # management of events
        for event in pygame.event.get():
            if event.type == QUIT:
                keep = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                keep = False
            elif event.type == KEYDOWN and event.key == K_SPACE:
                ave.fly()
        # add new floor every certain time
        Helper.add_floor(all, Floor())
        # actualize the screen
        all.update()
        all.clear(ventana, background)
        pipes.clear(ventana, background)
        dirty_rects = pipes.draw(ventana)
        dirty_rects += all.draw(ventana)
        if dirty_rects:
            pygame.display.update(dirty_rects)
            dirty_rects = None
        aps = reloj.tick(FPS)
        ave.aps = aps
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
