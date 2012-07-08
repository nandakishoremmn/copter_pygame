'''
Created on 07-Jul-2012

@author: TOSHIBA
'''

from initialise import screen, WIDTH, HEIGHT
from pygame import image, display, key, draw
from pygame.constants import K_SPACE, K_UP
from gameobjects.vector2 import Vector2
from random import randint

class PLAYER():
    '''
        Class for the player object
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.pic = image.load('images/planet.png')
        self.tail_pic = image.load('images/tail.png')
        self.size = Vector2(self.pic.get_width(),self.pic.get_height())
        self.position = Vector2(.1*WIDTH,.5*HEIGHT)
        self.velocity = Vector2()
        self.tail = [.5*HEIGHT]*40
        
     
    def move(self):
        keys = key.get_pressed()
        for k in [K_SPACE,K_UP]:
            if keys[k]:
                self.velocity.y = min(0,self.velocity.y-.1)
                self.position.y += self.velocity.y
                break
        else:
            self.velocity.y = max(-3,self.velocity.y+.1)
            self.position.y += self.velocity.y
        if randint(1,1)==1:
            self.tail = self.tail[1:]
            self.tail.append(self.position.y)
  
    def draw(self):
        screen.blit(self.pic, (self.position-self.size/2) )
        for i, t in enumerate(self.tail[::4]):
            screen.blit(self.tail_pic, map(int, ((i-3)*.01*WIDTH,t-10)) )
            #draw.circle( screen, (255,255,0,0),map(int, ((i-1)*.01*WIDTH,t)),int(15-i*.4) )
        #x, y = self.position - self.size/2
        #w, h = self.size
        #display.update([[x, y], [w, h]])