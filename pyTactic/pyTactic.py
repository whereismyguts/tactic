import sys
import pygame
from Point import Point
from Unit import Unit
import time

class Main:
    def process_input(self):
        for event in pygame.event.get():
            self.text = "---"
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                self.text = "mouse at (%d, %d)" % event.pos
                if self.pressed:
                    self.d_x = event.pos[0]
                    self.d_y = event.pos[1]
                for u in self.units:
                    u.highlighted =  u.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.pressed = True
                    self.anc_x = self.d_x = event.pos[0]
                    self.anc_y = self.d_y = event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.pressed = False
                    self.select(event.pos)

                elif event.button == 3:
                    targets = None
                    active = list(filter(lambda x: x.selected, self.units))
                    if len(active) > 0:
                        targets = list(filter(lambda x: x.rect.collidepoint(event.pos), self.units))
                        if len(targets) > 0:
                            for u in active:
                                if u != targets[0]:
                                    u.target = targets[0]
                        else:
                            for u in active:
                                u.target = Point(event.pos)

    def update(self):
        # for i in range(len(self.units) - 1):
        #     self.units[i].target = self.units[i + 1].pos
        # self.units[len(self.units) - 1].target = self.units[0].pos
        for unit in self.units:
            unit.update(self.units)

        self.process_input()
            
        if self.pressed:
            self.sel_bottom = max(self.d_y,  self.anc_y)
            self.sel_top = min(self.d_y,  self.anc_y)
            self.sel_left = min(self.d_x,  self.anc_x)
            self.sel_right = max(self.d_x,  self.anc_x)        
            self.text = "lm button at (%d,%d):(%d,%d)" % (self.sel_left, self.sel_top, self.sel_right, self.sel_bottom)
        # if r(1, 150) == 5:
        #     units.append(Unit())

    def select(self, point):
        for unit in self.units:
            if  unit.rect.collidepoint(point) or self.sel_left <= unit.pos.x <= self.sel_right and self.sel_top <= unit.pos.y <= self.sel_bottom:
                unit.selected = True
            else : unit.selected = False

    def draw(self):
        self.screen.fill((255,255,255))    
        for unit in self.units:
            unit.draw(self.screen)

        # screen.blit(unit, unitrect)
        # self.text+=", fps: "+str( self.frame / (time.time() -
        # self.total_start))

        if self.pressed:
            pygame.draw.rect(
                self.screen,
                (0, 150, 0),
                pygame.Rect(self.sel_left,
                            self.sel_top,
                            self.sel_right - self.sel_left,
                            self.sel_bottom - self.sel_top), 1)

        textsurface = self.myfont.render(self.text, True, (255, 255, 255))

        self.screen.blit(textsurface,(10,10))
        pygame.display.flip()
    
    def __init__(self, **kwargs):
        # unit = pygame.image.load("unit.bmp")
        self.text = ""
        self.size = self.width, self.height = 500, 500    
        self.screen = pygame.display.set_mode(self.size)
        
        pygame.font.init()
        self.myfont = pygame.font.SysFont('impact', 15)
        spritesheet = pygame.image.load('zombie_0.png')

        self.units = []
        for i in range(10):
            self.units.append(Unit(spritesheet))
        
        self.frame = 0 
        self.updates = 0
        self.draw_loop_start = self.update_loop_start = self.total_start = time.time()

        fps = 60
        ups = 60

        self.seconds_per_frame = 1 / fps
        self.seconds_per_update = 1 / ups

        self.target = None
        self.pressed = False

        self.d_x = self.d_y = self.anc_x = self.anc_y = 0
        self.sel_top = self.sel_left = self.sel_bottom = self.sel_right = 0

    def start(self):
        while True:
            if(time.time() - self.update_loop_start >= self.seconds_per_update):
                self.update()
                self.updates += 1
                self.update_loop_start = time.time()
                # print ( updates / (time.time() - total_start))

            if(time.time() - self.draw_loop_start >= self.seconds_per_frame):
                self.draw() 
                self.frame += 1
                self.draw_loop_start = time.time()


if __name__ == '__main__':
    # pygame.init()
    # screen = pygame.display.set_mode((640, 480))
    # my_sprite = TestSprite()
    # my_group = pygame.sprite.Group(my_sprite)
    # while True:
    #    event = pygame.event.poll()
    #    if event.type == pygame.QUIT:
    #        pygame.quit()
    #        sys.exit(0)

    #    screen.fill((255,255,255))
    #    my_group.update()
    #    my_group.draw(screen)
    #    pygame.display.flip()

    pygame.init()        
    main = Main()
    main.start()