import pygame
# import time
# from random import randint as r


class ZombieSprite(pygame.sprite.Sprite):
    def __init__(self, y, frames, spritesheet, one_time = False ,start = 0):
        super(ZombieSprite, self).__init__()
        side = 128
        self.images = []
        self.one_time = one_time
        self.i = 0

        for x in frames:
            rect = pygame.Rect(side * x, y * side, side, side)
            #self.images.append(pygame.transform.scale(spritesheet.subsurface(rect), (100, 100)))
            self.images.append((spritesheet.subsurface(rect)))
        
        self.rect = pygame.Rect(0, 0, side , side )
        self.index = start
        self.image = self.images[self.index]
    
    def set_position(self, point):
        self.rect[0] = point.x - self.rect[2]/2
        self.rect[1] = point.y - self.rect[3]/2

    def update(self):
        if self.i == 6:
            self.i=0
            self.index += 1
            if self.index >= len(self.images):
                if self.one_time:
                    return
                self.index = 0
            self.image = self.images[self.index]

        self.i += 1
