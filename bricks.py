'''
Created on 07-Jul-2012

@author: TOSHIBA
'''

from initialise import screen, WIDTH, HEIGHT
from pygame import image, display, draw, Rect
from pygame.constants import K_SPACE
from gameobjects.vector2 import Vector2
from random import randint

SPEED = 2

class BRICK():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.pic = image.load('images/Asteroid.png')
        self.size = Vector2(self.pic.get_width(), self.pic.get_height())
        self.radius = randint(15,20)
        self.position = Vector2( WIDTH+self.radius, randint(0,HEIGHT-self.radius) )
        global SPEED
        self.velocity = Vector2(int(SPEED), 0)
        SPEED += .02
        
    def move(self):
        self.position -= self.velocity
  
    def draw(self):
        screen.blit(self.pic, (self.position-self.size/2) )
        #draw.circle( screen, (0,0,128), map(int, self.position), self.radius )