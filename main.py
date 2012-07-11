'''
Created on 07-Jul-2012

@author: NANDU
'''
from pygame import display, init, time, event, font, image, mixer
from pygame.constants import *
from player import PLAYER
from bricks import BRICK
import bricks
from add_score import post_score
from random import randint
from initialise import screen, WIDTH, HEIGHT
from pickle import dump, load 

class Game:
    def __init__(self):
        init()
        self.clock = time.Clock()
        self.n = 0  # Asteroid index
        self.pic = image.load('images/back.png').convert()  # background image
        self.quit, self.pause, self.stop = False, False, False
        self.score = 0
        self.inc = 1
        try:    # to read high score from file
            f=open('high.dat','r')
            self.high=load(f)
            f.close()
        except:
            self.high=0
        self.message = "Score : %3d    High : %3d"%(self.score,self.high)
        self.Font = font.SysFont("arial", 40)
        self.msg_center = "" 
        self.bricks = dict()
        self.player = PLAYER()
        self.tick = 100
        self.bg_x = 0
        self.rank = False
        self.bg_sfx = mixer.Sound('sounds/bg.wav')  # Background music

    def handle_events(self):    # handling keyboard
        for evt in event.get():
            if evt.type == QUIT:    # quit the game
                self.quit = True
            if evt.type == KEYDOWN:
                if evt.key == K_u and self.stop:
                    try:
                        if not self.rank:
                            r=str(post_score(self.player.name,self.score))
                            self.msg_center = 'Your Global Rank :'+r
                        self.rank = True
                    except:
                        self.rank = False
                        self.msg_center = 'Sorry! Failed to fetch rank'
                if evt.key == K_ESCAPE: # quit the game
                    self.quit = True
                if evt.key == K_p and not self.stop:  # press p for pause
                    self.pause = True
                    self.msg_center = "Press 'Space' to resume" 
                if evt.key == K_SPACE:  # press space to ...
                    if self.pause:  # ...unpause on pressing p
                        self.pause = False
                        self.msg_center = "" 
                    if self.stop:   #  ...start a new game if gameover
                        self.reset()
                        self.stop = False
                
    def put_message(self):
        '''
        Displays self.message
        '''
        self.message = "Score : %3d    High : %3d"%(self.score,self.high)
        text = self.Font.render(self.message, True, (0, 0, 255))    
        screen.blit(text, (WIDTH - 50 - text.get_width(),int(.9*HEIGHT)))
        
    def center_msg(self):
        '''
        Displays self.message
        '''
        text = self.Font.render(self.msg_center, True, (255, 0, 0))    
        screen.blit(text, (int(WIDTH-text.get_width())/2,int(HEIGHT-text.get_height())/2))
        
    def draw(self):
        '''
        Draws every thing on the screen
        '''
        screen.fill((0,0,0))    # Fill screen with black
        # Fill screen with background pattern
        for y in range(0, HEIGHT, self.pic.get_height()):
            for x in range(int(self.bg_x), WIDTH+self.pic.get_width(), self.pic.get_width()):
                screen.blit(self.pic, (x, y))
        for brick in self.bricks.values():  # Draws all the bricks
            brick.draw()
        self.player.draw()  # Draw the player
        self.put_message()
        self.center_msg()
        display.flip()  # Update the display

    def update(self):
        '''
        Changes position of all objects after every frame
        '''
        self.score += self.inc
        if self.score > self.high:
            self.high = self.score                                        
        # move the background
        if not ( self.pause or self.stop ):
            self.bg_x = self.bg_x-1 if self.bg_x > -self.pic.get_width() else 0
        if randint(1,20)==1:    # Bring a new asteroid with 1 in 20 probability
            self.n += 1
            self.bricks[self.n] = BRICK()
        for brick in self.bricks.values():
            brick.move()
        self.player.move()

    def check_bounds(self):
        self.tick, self.inc = 100, 1
        for index, brick in self.bricks.items():
            if brick.position.x + brick.radius < 0:
                del self.bricks[index]
            if ( brick.position-self.player.position ).length < ( brick.size.length/3 + self.player.size.length/3 ):
                self.player.pic = self.player.pic_dead
                self.player.sound.stop()
                self.player.explode.play()
                self.stop = True
                self.msg_center = "'Space'-New Game, 'U'-Upload Score"
            if ( brick.position-self.player.position ).length < ( brick.size.length/2 + self.player.size.length/2 ):
                self.tick,self.inc = 25, 4
                
        if not( self.player.size.y/2 < self.player.position.y < HEIGHT-self.player.size.y/2 ):
            self.player.pic = self.player.pic_dead
            self.player.sound.stop()
            self.player.explode.play()
            self.stop = True
            self.msg_center = "'Space'-New Game, 'U'-Upload Score"
    
    def reset(self):
        '''
        Reset objects for a new game
        '''
        bricks.SPEED = 2
        self.bricks = dict()
        self.player = PLAYER() 
        self.n = 0
        self.score = 0
        self.rank = False
        self.msg_center = ""
    
    def write_scores(self):
        '''
        Writes scores into the file
        '''
        f=open('high.dat','w')
        dump(self.high,f)
        f.close()   
        
    def run(self):
        '''
        Main loop
        '''
        self.bg_sfx.play(-1)
        self.bg_sfx.set_volume(01)
        while not self.quit:
            self.handle_events()
            if not (self.pause or self.stop):
                self.update()
                self.check_bounds()
            self.draw()
            self.clock.tick(self.tick)
        else:
            self.bg_sfx.stop()
            self.write_scores()
            
            
if __name__ == '__main__':
    game = Game()
    game.run()