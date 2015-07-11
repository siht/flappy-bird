'''
classes for some design patterns that are implemented
like plugins or are easy to implement
'''
from __future__ import print_function
from weakref import WeakKeyDictionary
from abc import ABCMeta, abstractmethod

class FlyWeight(type):
    '''
    copied of david villa
    http://crysol.org/es/user/3
    pattern flyweight as metaclass (level: aplication)
    add this metaclass in the definition of the class
    i.e.
    class A(object):
        __metaclass__ = FlyWeight
        ...
    '''
    def __init__(cls, name, bases, dct):
        cls.__instances = {}
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, key, *args, **kw):
        instance = cls.__instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kw)
            cls.__instances[key] = instance
        return instance

class Singleton(type):
    '''
    copied of david villa
    http://crysol.org/es/user/3
    pattern singleton as metaclass (level: aplication)
    add this metaclass in the definition of the class
    i.e.
    class A(object):
        __metaclass__ = Singleton
        ...
    '''
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance
