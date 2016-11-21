import pygame
from settings import *

class Tube:
    def __init__(self, surface, x, y, direction, offset, eligible):
        self.rectcolor = (255,0,255)
        self.surface = surface
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), (52, 640))
        self.direction = direction
        self.offset = offset
        self.eligible = eligible
    
    def draw(self):
        if self.direction == 1:
            drawing = TUBE2
            drawing = pygame.transform.scale(drawing, (52, 640))
        else:
            drawing = TUBE
            drawing = pygame.transform.scale(drawing, (52, 640-self.offset))
        self.surface.blit(drawing, (self.x, self.y))    
        #pygame.draw.rect(self.surface, self.rectcolor, self.rect)
    
    def event(self, playerdead, playercollided):
        if not playerdead and not playercollided:
            self.x -= TUBESPEED
            self.rect = pygame.Rect((self.x, self.y), (52, 640))
