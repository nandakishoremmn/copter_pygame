'''
Created on 07-Jul-2012

@author: NANDU
'''
from pygame import display, init, time, event, font
from pygame.constants import *
from player import PLAYER
from bricks import BRICK
import bricks
from random import randint
from initialise import screen, WIDTH, HEIGHT
from pickle import dump, load 

class Game:
    def __init__(self):
        init()
        self.clock = time.Clock()
        self.n = 0
        self.quit, self.pause, self.stop = False, False, False
        self.score = 0
        try:
            f=open('high.dat','r')
            self.high=load(f)
            f.close()
        except:
            self.high=0
        self.message = "Score : %3d    High : %3d"%(self.score,self.high)
        self.Font = font.SysFont("arial", 40);
        self.bricks = dict()
        self.player = PLAYER()

    def handle_events(self):
        for evt in event.get():
            if evt.type == QUIT:
                self.quit = True
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit = True
                if evt.key == K_p:
                    self.pause = True
                if evt.key == K_SPACE:
                    if self.pause:
                        self.pause = False
                    if self.stop:
                        self.reset()
                        self.stop = False
                
    def put_message(self):
        if not( self.pause or self.stop ):
            self.message = "Score : %3d    High : %3d"%(self.score,self.high)
        else:
            self.message = "Press 'Space'          Score : %3d    High : %3d"%(self.score,self.high)
        text = self.Font.render(self.message, True, (0, 0, 255))    
        screen.blit(text, (WIDTH - 50 - text.get_width(),int(.9*HEIGHT)))
        
    def draw(self):
        screen.fill((0,0,0))
        self.player.draw()
        for brick in self.bricks.values():
            brick.draw()
        self.put_message()
        display.flip()

    def update(self):
        self.score += 1
        if self.score > self.high:
            self.high = self.score
        if randint(1,20)==1:
            self.n += 1
            self.bricks[self.n] = BRICK()
        for brick in self.bricks.values():
            brick.move()
        self.player.move()

    def check_bounds(self):
        for index, brick in self.bricks.items():
            if brick.position.x + brick.radius < 0:
                del self.bricks[index]
            if ( brick.position-self.player.position ).length < ( brick.size.length/3 + self.player.size.length/3 ):
                self.stop = True
                
        if not( self.player.size.y/2 < self.player.position.y < HEIGHT-self.player.size.y/2 ):
            self.stop = True 
    
    def reset(self):
        bricks.SPEED = 2
        self.bricks = dict()
        self.player = PLAYER() 
        self.n = 0
        self.score = 0
    
    def write_scores(self):
        f=open('high.dat','w')
        dump(self.high,f)
        f.close()   
        
    def run(self):
        while not self.quit:
            self.handle_events()
            if not (self.pause or self.stop):
                self.update()
                self.check_bounds()
            self.draw()
            self.clock.tick(100)
        else:
            self.write_scores()
            
            
if __name__ == '__main__':
    game = Game()
    game.run()