'''
Created on 07-Jul-2012

@author: TOSHIBA
'''

from initialise import screen, WIDTH, HEIGHT
from pygame import image, display, key, draw, mixer
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
        try:
            f = open('name.txt')
            self.name = f.readline()
            f.close()
        except:
            self.name = 'New Player'
        self.pic_down = image.load('images/heli_down.png').convert_alpha()
        self.pic_up = image.load('images/heli_up.png').convert_alpha()
        self.pic_dead = image.load('images/explode.png').convert_alpha()
        self.pic = self.pic_down
        self.tail_pic = image.load('images/tail.png').convert_alpha()
        self.sound =  mixer.Sound('sounds/copter.wav');
        self.explode = mixer.Sound('sounds/end.wav')
        self.size = Vector2(self.pic.get_width(),self.pic.get_height())
        self.position = Vector2(.1*WIDTH,.5*HEIGHT)
        self.velocity = Vector2()
        self.tail = [.5*HEIGHT]*40
        mixer.Sound('sounds/start.wav').play()
        
     
    def move(self):
        keys = key.get_pressed()
        for k in [K_SPACE,K_UP]:
            if keys[k]:
                self.pic = self.pic_up
                self.sound.play()
                self.velocity.y = min(0,self.velocity.y-.1)
                self.position.y += self.velocity.y
                break
        else:
            self.sound.stop()
            self.pic = self.pic_down
            self.velocity.y = max(-3,self.velocity.y+.1)
            self.position.y += self.velocity.y
        if randint(1,1)==1:
            self.tail = self.tail[1:]
            self.tail.append(self.position.y)
  
    def draw(self):
        screen.blit(self.pic, (self.position-self.size/2) )
        for i, t in enumerate(self.tail[::4]):
            screen.blit(self.tail_pic, map(int, ((i-3)*.01*WIDTH,t-self.pic.get_width()/2)) )
            #draw.circle( screen, (255,255,0,0),map(int, ((i-1)*.01*WIDTH,t)),int(15-i*.4) )
        #x, y = self.position - self.size/2
        #w, h = self.size
        #display.update([[x, y], [w, h]])