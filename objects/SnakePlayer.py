import pygame
import main
from objects.BasicObject import BasicObject
from objects.Coin import Coin
from objects.Enemy import Enemy
from objects.MovingEnemy import MovingEnemy
from util.Controller import Controller
import numpy
class SnakePlayer(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        pygame.font.init()
        self.controller = Controller(False,False,False,False)
        self.head = None
        self.tail = None
        self.previousMove = Controller(False,False,False,False)
        self.segmentList = []
        self.generateTail = 0
        self.score = 0
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.gameOver = False
    def isOutOfBounds(self):
        
        return not self.rect.colliderect(pygame.Rect(0,0,800,600))
    def step(self):
        if self.tail is not None and self.gameOver == False:
            self.previousMove.copyTo(self.tail.controller)
        if  self.gameOver == False:
            if self.controller.right:
                self.rect.left+=1
            if self.controller.left:
                self.rect.left-=1
            if self.controller.up:
                self.rect.top-=1
            if self.controller.down:
                self.rect.top+=1
        self.controller.copyTo(self.previousMove)
        
        
        
        for a in self.segmentList:
            a.step()
            
            
            if a.isOutOfBounds() and a.gameOver == False:
                
                self.score +=1
                a.gameOver = True
                
                
        if self.generateTail >0:
            self.addTail()
            self.generateTail-=1
            
        
        
        if self.isOutOfBounds() and self.head == None:
            self.gameOver = True
    def draw(self,surface):
       
        
        for a in self.segmentList:
            if a.gameOver == False:
                pygame.draw.ellipse(surface, (255, 255, 0), a.rect)
        if self.gameOver == False:
            pygame.draw.ellipse(surface, (0, 255, 0), self.rect)
        status = "Score: "+str(self.score)
        if self.gameOver:
            status = status +" Gameover!"
        text_surface = self.font.render(status, False, (255, 255, 255))
        surface.blit(text_surface, (0,0))
        
    def collision(self,gameObjects):
        for a in gameObjects:
            #check segment collision
            if type(a) == MovingEnemy and a.active == True:
                for segment in self.segmentList:
                    #check if segments collide with enemy
                    if segment.rect.colliderect(a):
                        
                        #deactivate enemy and split tail
                        segment.tail = None
                        
                        a.active = False
                        break
            if a.active == False or self.rect.colliderect(a) == False:
                continue
            if type(a) == Coin and self.head == None:
                self.generateTail = 10
                
                a.active = False
            elif type(a) == MovingEnemy:
                if self.head == None:
                    self.gameOver = True
                    #recursively stop tails
                    t = self.tail
                    while t != None:
                        t.gameOver = True
                        t = t.tail
            
                
            
    
    def addTail(self,newTail = None):
        #make tail if none provided
        if newTail == None:
            
            newTail = SnakePlayer(pygame.Rect(0,0,10,10))
            
            self.segmentList.append(newTail)
        v = self.controller.getMovementVectors()
        newTail.rect.left = self.rect.left-v[0]
        newTail.rect.top = self.rect.top-v[1]
        #set tail to self if it is avaliablt. 
        if self.tail == None:
            newTail.head = self
            self.tail = newTail
            
        else:
            #otherwise tell tail to add new tail.
            self.tail.addTail(newTail)
    