from __future__ import print_function
from patterns import FlyWeight, typewrapper
from utils import load_img, Surfaces
import pygame
from preferences import *
import time
import pytweener

@typewrapper(pygame.surface.Surface, '_surf')
class SurfaceImage(object):
    '''wrapper of a basic Surface of pygame only for images'''
    __metaclass__ = FlyWeight
    def __init__(self, path):
        self._surf = load_img(path)

    wrap = property(lambda self: self._surf)

class Bird(pygame.sprite.Sprite):
    '''animation for presentation'''
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN0 = 'DOWN0'
    DOWN1 = 'DOWN1'
    FACES = RIGHT, UP, DOWN0, DOWN1
    
    def __init__(self, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.images = {Bird.RIGHT:[]}
        aux = SurfaceImage('bird1.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        self.images[Bird.RIGHT].append(aux)
        aux = SurfaceImage('bird2.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        self.images[Bird.RIGHT].append(aux)
        aux = SurfaceImage('bird3.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        self.images[Bird.RIGHT].append(aux)
        ##
        self.images.update({Bird.UP:[]})
        aux = SurfaceImage('bird1.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, 30)
        self.images[Bird.UP].append(aux)
        aux = SurfaceImage('bird2.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, 30)
        self.images[Bird.UP].append(aux)
        aux = SurfaceImage('bird3.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, 30)
        self.images[Bird.UP].append(aux)
        ##
        self.images.update({Bird.DOWN0:[]})
        aux = SurfaceImage('bird1.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -30)
        self.images[Bird.DOWN0].append(aux)
        aux = SurfaceImage('bird2.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -30)
        self.images[Bird.DOWN0].append(aux)
        aux = SurfaceImage('bird3.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -30)
        self.images[Bird.DOWN0].append(aux)
        ##
        self.images.update({Bird.DOWN1:[]})
        aux = SurfaceImage('bird1.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -90)
        self.images[Bird.DOWN1].append(aux)
        aux = SurfaceImage('bird2.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -90)
        self.images[Bird.DOWN1].append(aux)
        aux = SurfaceImage('bird3.png')
        aux = Surfaces.scale(aux.wrap, BIRD_SIZE)
        aux = Surfaces.rotate(aux, -90)
        self.images[Bird.DOWN1].append(aux)

        self.__index_image = 0
        self.__inc = True
        self.__want_flap = 0
        self.__flap_delay = 2
        self.__facing = Bird.FACES[0]
        self.__wants_fly = False
        self._my_tweener = pytweener.Tweener()
        self.__aps = 0
        self.__im_flying = True

        self.image = self.images[self.__facing][self.__index_image]
        self.rect = self.image.get_rect()
        self._x, self._y = position
        self.rect.topleft = position
        
    @property
    def aps(self):
        return self.__aps

    @aps.setter
    def aps(self, value):
        self.__aps = value

    def move_wings(self):
        if self.__index_image == 2:
            self.__inc = False
        if self.__index_image == 0:
            self.__inc = True
        if self.__inc:
            self.__index_image += 1
        else:
            self.__index_image -= 1
        self.image = self.images[self.__facing][self.__index_image]

    def fly(self):
        if self._my_tweener.hasTweens():
            self._my_tweener = pytweener.Tweener()
        up = SIZE_FLY
        easing_object = self
        y = self.rect.y + up
        tw_time = TIME_FLY
        # tw_type = pytweener.Easing.Linear.easeNone
        # tw_type = pytweener.Easing.Bounce.easeOut
        tw_type = pytweener.Easing.Elastic.easeOut
        # tw_type = pytweener.Easing.Expo.easeOut
        self._my_tweener.addTween(easing_object,
                                  _y=y,
                                  tweenTime=tw_time,
                                  tweenType=tw_type,
                                  onCompleteFunction=easing_object.fall)
        self.__facing = Bird.UP
        self.__im_flying = True

    def fall(self):
        self._my_tweener = pytweener.Tweener()
        self.__im_flying = False
        self.__facing = Bird.DOWN0
        down = FLOOR_LEVEL
        easing_object = self
        y = down - self.rect.y
        tw_time = TIME_FLY
        tw_type = pytweener.Easing.Linear.easeIn
        print(down, y, tw_time, tw_type)
        self._my_tweener.addTween(easing_object,
                                  _y=y,
                                  tweenTime=tw_time,
                                  tweenType=tw_type)

    def keep_falling(self):
        delta = self.aps/1000.0
        self._my_tweener.update(delta)
        self.rect.y = self._y

    def keep_flying(self):
        delta = self.aps/1000.0
        self._my_tweener.update(delta)
        self.rect.y = self._y
        
    def update(self):
        self.__want_flap += 1
        if self.__want_flap == self.__flap_delay:
            self.__want_flap = 0
            self.move_wings()
        if self._my_tweener.hasTweens() and self.__im_flying:
            self.keep_flying()
        elif self._my_tweener.hasTweens() and not self.__im_flying:
            self.keep_falling()
        print(self.rect, self._y)

class BackGround(pygame.sprite.Sprite):
    '''BackGround is always static'''
    def __init__(self, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = SurfaceImage('background.png').wrap
        self.image = Surfaces.scale(self.image,
                                    (WINDOW_SIZE[0] + 9, WINDOW_SIZE[1] - 100)
                                   )
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Logo(pygame.sprite.Sprite):
    '''logo is only for presentation'''
    def __init__(self, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = SurfaceImage('logo.png').wrap
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class Pipe(pygame.sprite.Sprite):
    '''static tube, only for presentation'''
    def __init__(self, position=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = SurfaceImage('pipe.png').wrap
        self.image = Surfaces.scale(self.image, TUBE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class PipeInverted(Pipe):
    '''inverted tube, only for presentation'''
    def __init__(self, position=(0,0)):
        Pipe.__init__(self, position)
        self.image = Surfaces.flip(self.image, False, True)

class Floor(pygame.sprite.Sprite):
    '''always changing'''
    def __init__(self, position=(WINDOW_SIZE[0] + 25, 500)):
        pygame.sprite.Sprite.__init__(self)
        self.image = SurfaceImage('ground.png').wrap
        self.image = Surfaces.scale(self.image, FLOOR_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def update(self):
        self.rect.x -= FLOOR_TIME
        if self.rect.x < -20:
            self.remove(self.groups())
            del(self)