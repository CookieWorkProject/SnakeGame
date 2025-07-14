import pygame
import math
class BasicObject:
    def __init__(self, rect):
        self.rect = rect
        self.active = True

    def step(self):
        pass
    def draw(self):
        pass
    def collision(self,gameObjects):
        pass
    def getCenterX(self):
        return self.rect.left+self.rect.width/2
    def getCenterY(self):
        return self.rect.top+self.rect.height/2
    def angle_between_vectors_degrees(self,u, v):
        dot_product = sum(i*j for i, j in zip(u, v))
        norm_u = math.sqrt(sum(i**2 for i in u))
        norm_v = math.sqrt(sum(i**2 for i in v))
        cos_theta = dot_product / (norm_u * norm_v)
        angle_rad = math.acos(cos_theta)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
    def getAxisDistToObjectX(self,other):
        return other.getCenterX()-self.getCenterX()
    def getAxisDistToObjectY(self,other):
        return other.getCenterY()-self.getCenterY()