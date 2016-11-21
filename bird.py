import pygame
from settings import *

class Bird:
    def __init__(self, surface, x, y):
        self.rectcolor = (0,255,255)
        self.dead = False
        self.surface = surface
        self.collided = False
        self.x = x
        self.y = y
        self.animationtimer = 0
        self.sprite = 1
        self.drawing = BIRD0
        self.rect = self.drawing.get_rect() 
        self.fallingspeed = 0
        self.upwardspeed = 0
        self.rotation = 0

    def event(self):
        if not self.dead and self.upwardspeed <= 0:
            self.y += self.fallingspeed
            self.rect.move(0, self.y)
        elif self.upwardspeed > 0:
            self.y -= self.upwardspeed
            self.rect.move(0, self.y)
            self.upwardspeed -= 1 

    def draw(self):
        self.animationtimer += 1
        if self.animationtimer >= 10 and not self.dead:
            self.sprite += 1
            if self.sprite >= 3:
                self.sprite = 0
            self.animationtimer = 0    
        if self.sprite == 0:
            self.drawing = pygame.transform.rotate(BIRD0, self.rotation)
        elif self.sprite == 1:
            self.drawing = pygame.transform.rotate(BIRD1, self.rotation)
        else:
            self.drawing = pygame.transform.rotate(BIRD2, self.rotation)
        self.surface.blit(self.drawing, (self.x, self.y))
        self.rect = self.drawing.get_rect(center=(self.x+20, self.y+20))
        #pygame.draw.rect(self.surface, self.rectcolor, self.rect)
