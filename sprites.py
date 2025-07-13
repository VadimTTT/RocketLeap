# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from random import randint
from config import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def move_x(self, x):
        self.x += x
        self._move()

    def move_y(self, y):
        self.y += y
        self._move()

    def set_x(self, x):
        self.x = x
        self._move()

    def set_y(self, y):
        self.y = y
        self._move()

    def _move(self):
        self.rect.center = (self.x, self.y)

    def init_image(self, img_path):
        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class Star(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.init_image('img/star.png')
        self.angle = 0
        self.original_image = self.image
    
    def update(self):
        self.angle = (self.angle + 2) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Monster(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.init_image('img/monster.png')

    def move(self):
        self.move_x(randint(-5, 5))
        self.move_y(randint(-5, 5))

class Doodle(Sprite):
    def __init__(self, name, character_img='img/rocket3.png'):
        super().__init__(doodle_start_position[0], doodle_start_position[1])
        self.name = name
        self.score = 0
        self.alive = 1
        self.ySpeed = 5
        
        self.img_r = pygame.image.load(character_img).convert()
        self.img_l = pygame.transform.flip(self.img_r, True, False)
        self.image = self.img_r
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def _move(self):
        self.rect.center = (self.x, self.y)
        if self.y >= screen_height:
            self.alive = 0

    def get_legs_rect(self):
        left = self.rect.left + self.rect.width * 0.1
        top = self.rect.top + self.rect.height * 0.9
        width = self.rect.width * 0.6
        height = self.rect.height * 0.1
        return pygame.Rect(left, top, width, height)

    def set_x(self, x):
        if x < self.x:
            self.image = self.img_l
        elif x > self.x:
            self.image = self.img_r
        self.x = x
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self._move()

    def inc_y_speed(self, speed):
        self.ySpeed += speed

    def inc_score(self, score):
        self.score += score

class Platform(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        if type(self).__name__ == "Platform":
            self.image = pygame.image.load('img/platform2.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)
            self.mask = pygame.mask.from_surface(self.image)
            rnd = randint(-100, 100)
            self.spring = Spring(self.x + randint(-platform_width//2 + 10, platform_width//2 - 10), 
                               self.y - 20) if rnd >= 0 else None
            self.star = Star(self.x, self.y - 30) if randint(0, 4) == 0 else None

    def get_surface_rect(self):
        return pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            self.rect.height * 0.1
        )

class MovingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('img/moving1.png').convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.way = -1
        self.xSpeed = randint(2, 6)
        self.spring = None
        self.star = None

    def move(self):
        self.move_x(self.xSpeed * self.way)
        if 10 < self.x < 19 or 460 < self.x < 469:
            self.way *= -1

class CrashingPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('img/broken1.png').convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.ySpeed = 10
        self.crashed = 0
        self.spring = None
        self.star = None

    def crash(self):
        self.init_image('img/brownplatformbr.png')
        self.crashed = 1

    def move(self):
        if self.crashed == 1:
            self.move_y(self.ySpeed)

class Spring(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.compressed = 0
        self.init_image('img/spring.png')

    def compress(self):
        self.init_image('img/spring_comp.png')
        self.compressed = 1

    def get_top_surface(self):
        return pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            self.rect.height * 0.1
        )

class Button(Sprite):
    def __init__(self, x, y, text):
        super().__init__(x, y)
        self.img_sel = pygame.image.load('img/menu_selected.png').convert()
        self.img_unsel = pygame.image.load('img/menu_unselected.png').convert()
        self.textSprite = TextSprite(self.x, self.y, text)
        self.changeState(0)

    def changeState(self, state):
        if state == 0:
            self.image = self.img_unsel
            self.textSprite.setColor((255, 165, 149))
        elif state == 1:
            self.image = self.img_sel
            self.textSprite.setColor((243, 227, 200))
        self.image.set_colorkey(self.image.get_at((0, 0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)



class CharacterSelectButton(Button):
    def __init__(self, x, y, character_img):
        try:
            self.character_img = character_img
            self.original_image = pygame.image.load(character_img).convert()
            
            scale_factor = 120 / self.original_image.get_height()
            new_width = int(self.original_image.get_width() * scale_factor)
            self.character_image = pygame.transform.scale(self.original_image, 
                                                        (new_width, 120))
            
            self.character_image.set_colorkey(self.character_image.get_at((0, 0)), RLEACCEL)
            self.rect = self.character_image.get_rect(center=(x, y))
            self.full_rect = pygame.Rect(x-60, y-70, 120, 140) 
        except:
            self.character_image = pygame.Surface((100, 120), pygame.SRCALPHA)
            pygame.draw.rect(self.character_image, (255, 0, 0), (0, 0, 100, 120), 2)
            self.rect = self.character_image.get_rect(center=(x, y))
            self.full_rect = pygame.Rect(x-60, y-70, 120, 140)
            self.character_img = None
    
    def draw(self, surface):
        surface.blit(self.character_image, self.rect)
    
    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

class Rectangle(pygame.Surface):
    def __init__(self, width, height, color):
        super().__init__((width, height), pygame.SRCALPHA)
        self.fill(color)

class TextSprite(Sprite):
    def __init__(self, x, y, text='', size=35, color=(255, 255, 255), icon=None):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.text = text
        self.icon = icon
        if self.icon:
            self.icon_image = pygame.image.load(icon).convert()
            self.icon_image.set_colorkey(self.icon_image.get_at((0, 0)), RLEACCEL)
        self.generateImage()

    def setText(self, text):
        self.text = text
        self.generateImage()

    def setColor(self, color):
        self.color = color
        self.generateImage()

    def setSize(self, size):
        self.font = pygame.font.Font(None, size)
        self.generateImage()

    def generateImage(self):
        text_surface = self.font.render(self.text, True, self.color)
        
        if self.icon:
            total_width = self.icon_image.get_width() + 10 + text_surface.get_width()
            max_height = max(self.icon_image.get_height(), text_surface.get_height())
            self.image = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
            self.image.blit(self.icon_image, (0, (max_height - self.icon_image.get_height()) // 2))
            self.image.blit(text_surface, (self.icon_image.get_width() + 10, 
                                         (max_height - text_surface.get_height()) // 2))
        else:
            self.image = text_surface
            
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)