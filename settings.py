import pygame

#Screen settings
WIDTH = 540 
HEIGHT = 760 
FPS = 60

#Asset settings
BIRD0 = pygame.image.load("assets/bird0.png")
BIRD1 = pygame.image.load("assets/bird1.png")
BIRD2 = pygame.image.load("assets/bird2.png")
BACKGROUND = pygame.image.load("assets/bg.png")
TUBE = pygame.image.load("assets/tube.png")
TUBE2 = pygame.image.load("assets/tube2.png")
GROUND = pygame.image.load("assets/ground.png")
GAMEOVER = pygame.image.load("assets/gameover.png")

#Game settings
GRAVITY = 0.5 
JUMPHEIGHT = 50 
TUBESPEED = 5
TUBEFREQ = 3
