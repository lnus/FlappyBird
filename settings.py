import pygame

#Screen settings
WIDTH = 540 
HEIGHT = 760 
FPS = 60

#Asset settings
BIRD = pygame.image.load("assets/bird.png")
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
