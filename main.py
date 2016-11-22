import pygame
from random import *
from settings import *
from tube import *
from bird import *

pygame.init()

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
        self.player = Bird(self.surface, (WIDTH/2)-20,HEIGHT/2-60)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Flapper")

    def restart(self):
        self.player = Bird(self.surface, (WIDTH/2)-20,HEIGHT/2-60)
        self.tubes = []
        self.points = 0

    def mainloop(self):
	#TODO: Optimize the tubes
        while True:
            self.tubetimer += 1
            if self.tubetimer >= 180/TUBEFREQ:
                self.tubetimer = 0
                tubeheight = randint(-100,100)
                tubeoffset = randint(25, 50)
                self.tubes.append(Tube(self.surface, WIDTH, ((HEIGHT/2)-tubeheight)+tubeoffset, 0, tubeoffset, True))
                self.tubes.append(Tube(self.surface, WIDTH, ((0-tubeheight)-320)-tubeoffset, 1, tubeoffset, False))
            self.event()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

    def event(self):    
        self.tubeController()
        self.applyGravity()
        if self.outOfBounds(): self.dead() 
        self.player.event()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.player.dead and not self.player.collided:
                #JUMP
                #TODO: Add sound when jumping
                self.player.fallingspeed = 0
                if self.player.rotation <= 10:
                    self.player.upwardspeed = 12 
                    for i in range(30):
                        self.player.rotation += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.player.dead:
                #RESTART
                self.restart()
                
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
            
    def tubeController(self):
        for tube in self.tubes:
            self.tubeCollision(tube)
            self.deleteTubes(tube)
            self.addPoints(tube)
            tube.event(self.player.dead, self.player.collided)

    def deleteTubes(self, tube):
        if tube.x <= -50:
            self.tubes.remove(tube)

    def tubeCollision(self, tube):
        if tube.rect.colliderect(self.player.rect) and not GODMODE:
            self.player.collided = True

    def addPoints(self, tube):
        #TODO: Add a sound when point is added
        if tube.x == WIDTH/2 and tube.eligible:
            tube.eligible = False
            self.points += 1

    def applyGravity(self):
        if self.player.rotation >= -60: 
            self.player.rotation -= 1.5 
        if self.player.fallingspeed < 100 and self.player.upwardspeed <= 0:    
            self.player.fallingspeed += GRAVITY    

    def outOfBounds(self):
        if self.player.y <= 0:
            return True
        elif self.player.y >= HEIGHT-105:
            return True
        else:
            return False

    def dead(self):
        if not GODMODE:
            self.player.dead = True

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

game = Flappy()
game.mainloop()
