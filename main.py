import pygame, sys
from pygame.locals import *
from graphics import Bird, BackGround, Pipe, PipeInverted, Floor, Logo
from preferences import *
from random import randint

MESSAGE = 'PRESS SPACE TO START'

class Helper(object):
    floor_time = FLOOR_TIME
    tube_spawn = TUBE_SPAWN
    

    @staticmethod
    def add_floor(obj, *groups):
        if Helper.floor_time == FLOOR_TIME:
            Helper.floor_time = 0
            for group in groups:
                group.add(obj)
        Helper.floor_time += 1

    @staticmethod
    def create_single_pipe(group):
        if Helper.tube_spawn == TUBE_SPAWN:
            Helper.tube_spawn = 0
            if randint(0,1):
                group.add(Pipe())
            else:
                group.add(PipeInverted())
        Helper.tube_spawn += 1

def main():
    pygame.init()
    ventana = pygame.display.set_mode(WINDOW_SIZE, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption('Flappy Bird')
    all = pygame.sprite.RenderUpdates()
    pipes = pygame.sprite.RenderUpdates()
    soil = pygame.sprite.Group()
    reloj = pygame.time.Clock()
    dirty_rects = None
    basicFont = pygame.font.SysFont(None, 24)
    text = basicFont.render(MESSAGE, True, BLANCO)
    

    # sprite statics
    background_game = pygame.Surface(ventana.get_size())
    background_intro = pygame.Surface(ventana.get_size())
    fondo = BackGround()
    logo = Logo((200, 200))
    tubo = Pipe((100, 400))
    tubo_i = PipeInverted((100, 0))
    
    # generate the backgrounds
    background_game.blit(fondo.image, fondo.rect)
    background_intro.blit(fondo.image, fondo.rect)
    background_intro.blit(tubo.image, tubo.rect)
    background_intro.blit(tubo_i.image, tubo_i.rect)
    background_intro.blit(logo.image, logo.rect)
    centro = list(ventana.get_rect().center)
    centro[0] -= 100
    centro[1] -= 150
    background_intro.blit(text, centro)
    # draw the background
    ventana.blit(background_intro, background_intro.get_rect())
    pygame.display.flip()
    # sprite animated
    ave = Bird((105, 330))
    all.add(ave)
    for i in range(0, 16):
        floor = Floor((WINDOW_SIZE[0] - 25*i, 500))
        all.add(floor)
        soil.add(floor)
        floor = None
        
    keep = True
    game_over = True
    change_state = False
    start = False
    while keep:
        if change_state:
            # bg = game_over and background_intro or background_game
            bg = background_game
            ventana.blit(bg, bg.get_rect())
            pygame.display.flip()
            change_state = False
            start = True
        # management of events
        if game_over:
            for event in pygame.event.get():
                if event.type == QUIT:
                    keep = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    keep = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    game_over = False
                    change_state = True
            # add new floor every certain time
            Helper.add_floor(Floor(), all, soil)
            # actualize the screen
            all.update()
            all.clear(ventana, background_intro)
            dirty_rects = all.draw(ventana)
            if dirty_rects:
                pygame.display.update(dirty_rects)
                dirty_rects = None
            aps = reloj.tick(FPS)
            ave.aps = aps
        else:
            if start:
                ave.fly()
                start = False
                pipes = pygame.sprite.RenderUpdates()
            for event in pygame.event.get():
                if event.type == QUIT:
                    keep = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    keep = False
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    ave.fly()
            if pygame.sprite.spritecollideany(ave, soil) or\
              pygame.sprite.spritecollideany(ave, pipes):
                ave.alive = False
                game_over = True
            # add new floor every certain time
            Helper.create_single_pipe(pipes)
            Helper.add_floor(all, Floor())
            # actualize the screen
            pipes.update()
            all.update()
            pipes.clear(ventana, background_game)
            all.clear(ventana, background_game)
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
