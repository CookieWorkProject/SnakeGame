import pygame
import numpy
from objects.BasicObject import BasicObject
class MovingEnemy(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        self.xVelo = 0
        self.yVelo = 0
        self.hp = 5
        self.knockback = 0
        self.knockbackX = 0
        self.knockbackY = 0
        self.knockbackPower = 0
        self.exp = 5
        self.movementx = 0
        self.movementy = 1
        #movemntTimer
        self.movementt= 30
        #movementMaxTimer
        self.movementm= 30
        self.speed = 2
    def step(self):
        if self.knockback>0:
            self.rect.left+=self.knockbackX*self.knockbackPower
            self.rect.top+=self.knockbackY*self.knockbackPower
            self.knockback-=1
            #stun eeffect
            if self.knockback<10:
                self.knockbackPower = 0
            
        self.rect.left+=self.movementx*self.speed
        self.rect.top+=self.movementy*self.speed
        self.movementt-=1
        if self.movementt<0:
            self.movementt=self.movementm
            self.movementx*=-1
            self.movementy*=-1
    def setKnockback(self,frames,x,y,power):
        self.knockback = frames
        self.knockbackX = x
        self.knockbackY = y
        self.knockbackPower = power
    def takeDamage(self,dam):
        self.hp = self.hp - dam
        
        if self.hp <= 0:
            self.active = False
        return not self.active
    def draw(self,surface):
        pygame.draw.ellipse(surface, (255, 0, 0), self.rect)
