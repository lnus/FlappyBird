import pygame
from random import *
from settings import *

pygame.init()

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
        self.rect = pygame.Rect((self.x, self.y-2), (30, 20))
        self.fallingspeed = 0
        self.upwardspeed = 0
        self.rotation = 0

    def event(self):
        if not self.dead and self.upwardspeed <= 0:
            self.rect = pygame.Rect((self.x, self.y-2), (30, 20))
            self.y += self.fallingspeed
        elif self.upwardspeed > 0:
            self.rect = pygame.Rect((self.x, self.y-2), (30, 20))
            self.y -= self.upwardspeed
            self.upwardspeed -= 1

    def draw(self):
        self.animationtimer += 1
        if self.animationtimer >= 10 and not self.dead:
            self.sprite += 1
            if self.sprite >= 3:
                self.sprite = 0
            self.animationtimer = 0    
        if self.sprite == 0:
            drawing = pygame.transform.rotate(BIRD0, self.rotation)
        elif self.sprite == 1:
            drawing = pygame.transform.rotate(BIRD1, self.rotation)
        else:
            drawing = pygame.transform.rotate(BIRD2, self.rotation)
        self.surface.blit(drawing, (self.x, self.y))
        #pygame.draw.rect(self.surface, self.rectcolor, self.rect)

class Flappy:
    def __init__(self):
        self.points = 0
        self.tubes = []
        self.tubetimer = 0
        self.groundstep = 0 
        self.backgroundstep = 0
        self.background = (randint(0,255), randint(0,255), randint(0,255))
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill(self.background)
        self.bgimage = pygame.transform.scale(BACKGROUND, (1080,760))
        self.ground = pygame.transform.scale(GROUND, (1080,112))
        self.player = Bird(self.surface, (WIDTH/2)-20,HEIGHT/2)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flapper")

    def restart(self):
        self.player = Bird(self.surface, (WIDTH/2)-20,HEIGHT/2)
        self.tubes = []
        self.points = 0

    def mainloop(self):
        while True:
            self.tubetimer += 1
            if self.tubetimer >= 180/TUBEFREQ:
                self.tubetimer = 0
                tubeheight = randint(-100,100)
                tubeoffset = randint(15, 60)
                self.tubes.append(Tube(self.surface, WIDTH, ((HEIGHT/2)-tubeheight)+tubeoffset, 0, tubeoffset, True))
                self.tubes.append(Tube(self.surface, WIDTH, ((0-tubeheight)-320)-tubeoffset, 1, tubeoffset, False))
            self.event()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

    def applyGravity(self):
        if self.player.rotation >= -60: 
            self.player.rotation -= 1.5 
        if self.player.fallingspeed < 100 and self.player.upwardspeed <= 0:    
            self.player.fallingspeed += GRAVITY    

    def tubeCollision(self):
        for tube in self.tubes:
            if tube.rect.colliderect(self.player.rect):
                self.player.collided = True

    def outOfBounds(self):
        if self.player.y <= 0:
            return True
        elif self.player.y >= HEIGHT-105:
            return True
        else:
            return False

    def dead(self):
        self.player.dead = True

    def event(self):    
        self.tubeCollision()
        self.deleteTubes()
        self.addPoints()
        self.applyGravity()
        if self.outOfBounds(): self.dead() 
        self.player.event()
        for tube in self.tubes:
            tube.event(self.player.dead, self.player.collided)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.player.dead and not self.player.collided:
                #JUMP
                #TODO: Add sound when jumping
                for i in range(JUMPHEIGHT*2):
                    self.player.fallingspeed = 0
                    if self.player.rotation <= 10:
                        for i in range(30):
                            self.player.rotation += 1
                        self.player.upwardspeed = 12 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player.dead:
                #RESTART
                self.restart()

    def addPoints(self):
        #TODO: Add a sound when point is added
        for tube in self.tubes:
            if tube.x == WIDTH/2 and tube.eligible:
                tube.eligible = False
                self.points += 1

    def deleteTubes(self):
        for tube in self.tubes:
            if tube.x <= -50:
                self.tubes.remove(tube)

    def groundMovement(self):
        if self.player.dead or self.player.collided:
            self.groundstep = self.groundstep
        elif self.groundstep == -540:
            self.groundstep = 0
        else:
            self.groundstep -= 1 

    def backgroundMovement(self):
        if self.player.collided or self.player.dead:
            self.backgroundstep = self.backgroundstep
        elif self.backgroundstep == -540:
            self.backgroundstep = 0
        else:
            self.backgroundstep -= 1

    def draw(self):
        font = pygame.font.Font("assets/flappy.TTF", 36)
        points = font.render("{}".format(self.points), 1, (255,255,255))
        outline = font.render("{}".format(self.points), 1, (0,0,0))
        self.groundMovement()
        self.backgroundMovement()
        self.surface.blit(self.bgimage, (self.backgroundstep,0))
        for tube in self.tubes:
            tube.draw()
        self.surface.blit(self.ground, (self.groundstep,HEIGHT-70))
        self.surface.blit(outline, ((WIDTH/2)+1, 61))
        self.surface.blit(points, (WIDTH/2, 60))
        self.player.draw()
        if self.player.dead:
            self.surface.blit(GAMEOVER, ((WIDTH/2)-96, 140))

game = Flappy()
game.mainloop()
