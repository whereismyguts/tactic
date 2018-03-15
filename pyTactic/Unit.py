from random import randint as r
from Point import Point
from ZombieSprite import ZombieSprite
import numpy as np
import math
import pygame




class Unit:

    def __init__(self, spritesheet):
        self.color = r(0,255), r(0,255), r(0,255)
        self.hp = 10
        self.speed = 0.5
        self.selected = False
        self.highlighted =  False
        self.target = None
        self.prevs = []
        self.pos = Point((r(10, 490),r(10, 490)))
        self.rotation = r(-314, 314)/100
        self.prev_counter = 0
        self.myfont = pygame.font.SysFont('impact', 15)
        self.hit_cooldown = 0
        self.state = States.Idle
        self.move_sprites = dict()
        self.idle_sprites = dict()
        self.hit_sprites = dict()
        self.death_sprites = dict()

        y = 0
        for i in range(-4,4):
            octa = i * math.pi / 4 
            self.hit_sprites[octa] = pygame.sprite.Group(
                ZombieSprite(y,range(12,21), spritesheet))
            self.move_sprites[octa] = pygame.sprite.Group(
                ZombieSprite(y,range(4,12), spritesheet, start=r(0,7)))
            self.idle_sprites[octa] = pygame.sprite.Group(
                ZombieSprite(y,range(4),spritesheet, start=r(0,3)))
            self.death_sprites[octa] = pygame.sprite.Group(
                ZombieSprite(y,range(28,36),spritesheet, one_time = True))
            y+=1

        octa = 4 * math.pi / 4 
        self.hit_sprites[octa] = pygame.sprite.Group(
            ZombieSprite(0,range(12,21), spritesheet))
        self.move_sprites[octa] = pygame.sprite.Group(
            ZombieSprite(0,range(4,12), spritesheet, start=r(0,7)))
        self.idle_sprites[octa] = pygame.sprite.Group(
            ZombieSprite(0,range(4),spritesheet, start=r(0,3)))
        self.death_sprites[octa] = pygame.sprite.Group(
            ZombieSprite(0,range(28,36),spritesheet, one_time = True))
    
    def get_rect(self):          
        return pygame.Rect(self.pos.x - 20, self.pos.y - 50, 40, 65)
    rect = property(get_rect, None, None, 'rect')

    
    
    def take_damage(self, dmg):
        if self.hp > 0:
            self.hp -= dmg
            if self.hp == 0:
                self.state = States.Death

    def update(self, units):
        if self.state == States.Death:
            return
        self.hit_cooldown += 1

        if self.target:
            target = None

            if isinstance(self.target, Unit):
                target = self.target.pos 
                if target.dist(self.pos) < 25:
                    if self.hit_cooldown > 50:
                        self.hit_cooldown = 0
                        self.state = States.Hit
                        self.target.take_damage(1)
                        if self.target.state == States.Death:
                            self.target = None
                    return
            else:
                target = self.target

            if target.dist(self.pos) < 25:
                self.state = States.Idle
                return
            points = {}
            for b in np.arange(0.0, math.pi * 2, math.pi / 4):
                point = Point((self.pos.x - math.sin(b) * -25, self.pos.y + math.cos(b) * -25))
                value = 0
                for u in units:
                    if u == self:
                        continue
                    d = point.dist(u.pos)
                    if d < 25:
                        value = -10
                        break
                # for w in self.walls:
                #    if w.collidepoint(point):
                #        value = -10
                #        break
                d = point.dist(target)
                if d > 0:
                    value += (100 / d) * 10
                if len(self.prevs) > 0:
                    for p in self.prevs:
                        pd = point.dist(p)
                        if pd < 100:
                            value += pd / 1000
                if value >= 0: 
                    points[point] = value
            if len(points) > 0:
                target = max(points, key= lambda p: points[p])
                self.move(target)
                self.state = States.Move
        else:
            self.state = States.Idle

    def draw(self, screen):
        #pygame.draw.ellipse(screen, self.color, self.rect)
        # for p in self.prevs:
        #     pygame.draw.ellipse(screen, self.color, (p, (10,10)), 2)
        #     pygame.draw.rect(screen, (0,255,0), self.rect, 1)

        if self.hp > 0:
            #pygame.draw.rect(screen, (0, 255, 0), (self.rect[0], self.rect[1]-50, self.rect[2] / 100 * self.hp, 5))
            #pygame.draw.rect(screen, (0, 0, 0), (self.rect[0]-1, self.rect[1]-50, self.rect[2]+1, 6), 1)
            if self.selected:
                pygame.draw.ellipse(screen, self.color, (self.pos - (20,10),( 40,20)), 1)
            if self.highlighted:
                pygame.draw.rect(screen, (0,255,0), self.rect,1)

        # if self.target:
        #    pygame.draw.ellipse(screen, self.color, (self.target, (10,10)), 2)
            #pygame.draw.line(screen, self.color, self.pos, self.pos +
            #(self.target-self.pos).normalize()*30, 1)

        #dir_vector = Point.get_rotated(Point((0,0)), self.rotation, 30)
        #pygame.draw.line(screen, (0, 0, 0), self.pos, self.pos + dir_vector, 1)

        # if self.state == States.Moving:
        #    self.draw_sprite(self.move_sprites, screen)
        # if self.state == States.Idle:
        #    self.draw_sprite(self.idle_sprites, screen)
        # if self.state == States.Hit:

        self.draw_sprite(getattr(self, self.state + '_sprites'), screen)
        # textsurface = self.myfont.render(str(self.rotation), True, (255, 255, 255))
        # screen.blit(textsurface, self.pos + Point((0,60)))

    def draw_sprite(self, sprites, screen):

        #for s in sprites.keys():
        #    group = sprites[s]
        #    sprite_pos = self.pos + Point((0, 50)).get_rotated(Point((0,0)), s, 50)
        #    group.sprites()[0].set_position(sprite_pos )
        #    textsurface = self.myfont.render(str(s), True, (0, 0, 0))
        #    group.update()
        #    group.draw(screen)
        #    screen.blit(textsurface, sprite_pos+Point((0,30)))
        #    pygame.draw.rect(screen, (0, 0, 0), group.sprites()[0].rect, 1)
        #return
        key = min(sprites.keys(), key=lambda p: abs(p - self.rotation))
        group = sprites[key]
        group.sprites()[0].set_position(self.pos-Point((0,30)))
        group.update()
        group.draw(screen)

    def __setattr__(self, name, value):
        if name == 'rotation':
            if value > math.pi:
                value = -math.pi
            elif value < -math.pi:
                value = math.pi
        return super().__setattr__(name, value)

    def move(self, target):
        target_vector = target - self.pos
        dir_vector = Point.get_rotated(Point((0,0)), self.rotation, 300)

        a = Point.angle(dir_vector, target_vector)
        if abs(a) < 0.3:
            self.pos+=dir_vector.normalize() * self.speed
        else:
            self.pos+=dir_vector.normalize() * self.speed * 0.5

        if a > 0: 
            self.rotation +=0.1
        else: 
            self.rotation -=0.1

        self.prev_counter +=1
        if self.prev_counter == 50:
            self.prevs.append(self.pos)
            if len(self.prevs) > 10:
                del self.prevs[0]
            self.prev_counter = 0

class States:
    Death = 'death'
    Idle = 'idle'
    Move = 'move'
    Hit = 'hit'