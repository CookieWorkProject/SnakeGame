import pygame

from objects.BasicObject import BasicObject
from objects.Coin import Coin
from objects.Enemy import Enemy
from util.Controller import Controller
import numpy
class Player(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        pygame.font.init()
        self.controller = Controller(False,False,False,False)
        self.hp = 3
        self.knockback = 0
        self.knockbackX = 0
        self.knockbackY = 0
        self.knockbackPower = 0
        self.experience = 0
        self.exp = 0
        self.font = pygame.font.SysFont('Times New Roman', 30)
        #value storing the minimum exp to reach a level
        self.levelReq = [0,3,9]

    def getLevel(self):
        if self.exp>self.levelReq[2]:
            return 3
        if self.exp>self.levelReq[1]:
            return 2
        return 1
    def getHPMax(self):
        if self.exp>self.levelReq[2]:
            return 7
        if self.exp>self.levelReq[1]:
            return 5
        return 3
    def getPower(self):
        return self.getLevel()
    def gainExp(self,exp):
        if exp <0:
            self.exp += exp
            if self.hp > self.getHPMax():
                self.hp = self.getHPMax()
            return
        
        if (self.exp +exp) >= self.levelReq[self.getLevel()]:
            self.exp += exp
            self.hp = self.getHPMax()
        else:
            self.exp += exp
            
    def step(self):
        if self.knockback>0:
            self.rect.left+=self.knockbackX*self.knockbackPower
            self.rect.top+=self.knockbackY*self.knockbackPower
            self.knockback-=1
            #stun eeffect
            if self.knockback<10:
                self.knockbackPower = 0
        else:
            if self.controller.right:
                self.rect.left+=1
            if self.controller.left:
                self.rect.left-=1
            if self.controller.up:
                self.rect.top-=1
            if self.controller.down:
                self.rect.top+=1
    def draw(self,surface):
        pygame.draw.ellipse(surface, (0, 255, 0), self.rect)
        status = "Level: "+str(self.getLevel())+"     HP: "+str(self.hp)
        text_surface = self.font.render(status, False, (255, 255, 255))
        surface.blit(text_surface, (0,0))
        
    def collision(self,gameObjects):
        for a in gameObjects:
            if a.active == False or self.rect.colliderect(a) == False or self.knockback>0:
                continue
            if type(a) == Coin:
                a.active = False
                
            elif type(a) == Enemy:
                #get vector from player to enemy
                x = self.getAxisDistToObjectX(a)
                y = self.getAxisDistToObjectY(a)
                #If the player isn't moving just take damage
                if self.controller.getMovementVectors() == (0,0):
                    self.setKnockback(30,-numpy.sign(x),-numpy.sign(y),3)
                    self.hp -=2
                    return
                
                angle = abs(self.angle_between_vectors_degrees(self.controller.getMovementVectors(),(x,y)))
                enemyDefeated = False
                if angle <15:
                    self.setKnockback(30,-numpy.sign(x),-numpy.sign(y),3)
                    self.hp -=1
                    self.gainExp(-1)
                    
                elif angle <30:
                    self.setKnockback(20,-numpy.sign(x),-numpy.sign(y),2)
                    self.hp -=1
                    enemyDefeated = a.takeDamage(self.getPower())
                    a.setKnockback(20,self.controller.getMovementVectors()[0],self.controller.getMovementVectors()[1],2)
                else:
                    enemyDefeated = a.takeDamage(self.getPower()*2)
                    a.setKnockback(30,self.controller.getMovementVectors()[0],self.controller.getMovementVectors()[1],3)
                    
                if enemyDefeated:
                    self.gainExp(a.exp)
                if self.hp <=0:
                    self.active = False
                
    def setKnockback(self,frames,x,y,power):
        self.knockback = frames
        self.knockbackX = x
        self.knockbackY = y
        self.knockbackPower = power