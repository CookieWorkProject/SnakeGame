import pygame
from objects.BasicObject import BasicObject
from objects.Player import Player
from objects.Enemy import Enemy
from objects.Coin import Coin
from util.Controller import Controller
from util.Controller import Controller




def startGame(gameObjects,replay,player,draw):
    
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    # Set up the game window
    if draw:
        screen = pygame.display.set_mode((800, 600))

    # Game loop
    running = True
    FramesSinceStart = 0
    FPS = 60
    clock = pygame.time.Clock()
    while running:
        
        if draw:
            screen.fill((0,0,0))
        if FramesSinceStart < len(replay):
            player.controller = replay[FramesSinceStart]
        else:
            running = False
            break
        for a in gameObjects:
            if a.active:
                a.step()
                a.collision(gameObjects)
                if draw:
                    a.draw(screen)
                
        
        if draw:
            pygame.display.update()
            pygame.display.set_caption(str(FramesSinceStart))
       
            
        FramesSinceStart +=1
        clock.tick(60)
    # Quit Pygame
    pygame.quit()
    return gameObjects


    
    
