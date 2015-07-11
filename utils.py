from __future__ import print_function
import os
import pygame

def load_img(name, extradir=''):
    '''load a image and optimize with or without alpha
    based on script of sjbrown
    http://ezide.com/games/writing-games.html'''
    if isinstance(name, list):
        fullname = 'data'
        for component in name:
            fullname = os.path.join(fullname, component)
    else:
        fullname = os.path.join('data', extradir, name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image

class Surfaces(object):
    '''class with helper methods(memoization)'''
    created = {}
    scaled = {}
    fliped = {}
    rotated = {}
    roto_zoomed = {}

    @staticmethod
    def listSurface(surface, sub_div):
        '''subdivide a Surface in one single list'''
        key = (surface, sub_div)
        if key not in Surfaces.created:
            tam = surface.get_width()//sub_div[0], surface.get_height()//sub_div[1]
            count = [0, 0]
            out = []
            while count[0] < sub_div[0]:
                count[1] = 0
                while count[1] < sub_div[1]:
                    cut_rect = (count[0] * tam[0], count[1] * tam[1], tam[0], tam[1])
                    out.append(surface.subsurface(cut_rect))
                    count[1] += 1
                count[0] += 1
            Surfaces.created.update({key: out})
            return out
        else:
            return Surfaces.created[key]

    @staticmethod
    def scale(surface, scale):
        '''scale a Surface'''
        key = (surface, scale)
        if key not in Surfaces.scaled:
            out = pygame.transform.scale(surface, scale)
            Surfaces.scaled.update({key : out})
            return out
        else:
            return Surfaces.scaled[key]

    @staticmethod
    def flip(surface, xbool, ybool):
        '''scale a Surface'''
        key = (surface, xbool, ybool)
        if key not in Surfaces.scaled:
            out = pygame.transform.flip(surface, xbool, ybool)
            Surfaces.fliped.update({key : out})
            return out
        else:
            return Surfaces.fliped[key]

    @staticmethod
    def rotate(surface, angle):
        '''rotate a Surface'''
        key = (surface, angle)
        if key not in Surfaces.rotated:
            out = pygame.transform.rotate(surface, angle)
            Surfaces.rotated.update({key : out})
            return out
        else:
            return Surfaces.rotated[key]

    @staticmethod
    def rotozoom(surface, angle, scale):
        '''rotate a Surface'''
        key = (surface, angle, scale)
        if key not in Surfaces.roto_zoomed:
            out = pygame.transform.rotozoom(surface, angle, scale)
            Surfaces.roto_zoomed.update({key : out})
            return out
        else:
            return Surfaces.roto_zoomed[key]

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    print("didn't expect that!")
