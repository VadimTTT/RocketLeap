# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sprites import Doodle, Platform, MovingPlatform, CrashingPlatform, Rectangle, Button, TextSprite, Spring, Monster, Star, CharacterSelectButton
import sys
from random import randint
import inputbox
from inputbox import ask
from config import *

class Location(object):
    parent = None
    def __init__(self, parent):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load('img/background.png').convert()
    def event(self,event):
        pass
    def draw(self):
        pass

class StartLocation(Location):
    def __init__(self, parent):
        Location.__init__(self, parent)
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(0)
        
        self.available_characters = [
            'img/rocket3.png',
            'img/character1.png', 
            'img/character2.png'
        ]
        self.selected_character = self.available_characters[0]
        
        self.title = TextSprite(
            screen_width // 2,
            50,
            "Rocket Leap",
            72,
            (255, 215, 0) 
        )
        
        self.char_positions = [
            (screen_width * 1/4, 200), 
            (screen_width * 2/4, 200),  
            (screen_width * 3/4, 200)
        ]
        
        self.char_buttons = []
        for i, char_img in enumerate(self.available_characters):
            btn = CharacterSelectButton(
                self.char_positions[i][0],
                self.char_positions[i][1],
                char_img
            )
            self.char_buttons.append(btn)
        
        self.startbtn = Button(screen_width//2, 320, "Start")
        self.exitbtn = Button(screen_width//2, 390, "Exit")
        
        self.controls = pygame.sprite.Group(self.startbtn, self.exitbtn)
        self.controls_captions = pygame.sprite.Group(
            self.startbtn.textSprite,
            self.exitbtn.textSprite
        )
        
        self.selection_surface = pygame.Surface((140, 160), pygame.SRCALPHA)
        pygame.draw.rect(self.selection_surface, (255, 215, 0), (0, 0, 140, 160), 3)
        
        self.selection_pos = self.char_positions[0]
    
    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.title.image, self.title.rect)
        choose_text = TextSprite(
            screen_width//2, 
            105,
            "Выберите персонажа",
            30,
            (255, 255, 255)
        )
        self.window.blit(choose_text.image, choose_text.rect)
        frame_x = self.selection_pos[0] - 70  # 140/2
        frame_y = self.selection_pos[1] - 80  # 160/2
        self.window.blit(self.selection_surface, (frame_x, frame_y))
        
        for btn in self.char_buttons:
            char_x = btn.rect.centerx - btn.character_image.get_width() // 2
            char_y = btn.rect.centery - btn.character_image.get_height() // 2
            self.window.blit(btn.character_image, (char_x, char_y))
        
        self.controls.draw(self.window)
        self.controls_captions.draw(self.window)
    
    def event(self, event):
        if event.type == MOUSEMOTION:
            for btn in self.controls:
                if btn.rect.collidepoint(pygame.mouse.get_pos()):
                    btn.changeState(1)
                else:
                    btn.changeState(0)
        
        elif event.type == MOUSEBUTTONUP:
            for i, btn in enumerate(self.char_buttons):
                if btn.full_rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected_character = btn.character_img
                    self.selection_pos = self.char_positions[i]
            
            if self.startbtn.rect.collidepoint(pygame.mouse.get_pos()):
                name = inputbox.ask(self.window, "Your name")
                if name:
                    self.parent.location = GameLocation(
                        self.parent, 
                        name, 
                        self.selected_character
                    )
            elif self.exitbtn.rect.collidepoint(pygame.mouse.get_pos()):
                sys.exit()

class GameLocation(Location):
    def __init__(self, parent, name, character_img = 'img/rocket3.png'):
        Location.__init__(self, parent)
        pygame.key.set_repeat(10)
        pygame.mouse.set_visible(0)
        self.doodle = Doodle(name, character_img)
   
        self.doodle = Doodle(name, character_img)
        self.doodle.name = name

        self.allsprites = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.allsprites.add(self.doodle)
    
        for i in range(0, platform_count):
            platform = self.randomPlatform(False)
            self.allsprites.add(platform)
            if isinstance(platform, Platform):
                if platform.spring:
                    self.allsprites.add(platform.spring)
                if platform.star:
                    self.allsprites.add(platform.star)
                    self.stars.add(platform.star)
    
        self.score_sprite = TextSprite(50, 25, f"{name}, 0", 45, (255, 255, 255))
        self.star_count = 0
        self.star_counter_sprite = TextSprite(
            screen_width - 100, 
            25, 
            str(self.star_count), 
            40, 
            (255, 255, 0), 
            'img/star.png'  
        )
        self.allsprites.add(self.score_sprite)
        self.allsprites.add(self.star_counter_sprite)
    
        self.window.blit(self.background, (0, 0))
    
        self.jump_sound = pygame.mixer.Sound("sounds/jump.wav")
        self.broke_sound = pygame.mixer.Sound("sounds/broke.wav")
        self.star_sound = pygame.mixer.Sound("sounds/star.wav") if pygame.mixer else None
    
        self.monster = None
        self.character_img = character_img 


    def randomPlatform(self, top=True):
        x = randint(0, screen_width - platform_width)
        bad_y = []
        for spr in self.allsprites:
            bad_y.append((spr.y-platform_y_padding, spr.y + platform_y_padding + spr.rect.height))

        good = 0
        while not good:
            if top:
               y = randint(-100, 50)
            else:
                y = randint(0, screen_height)
            good = 1
            for bad_y_item in bad_y:
                if bad_y_item[0] <= y <= bad_y_item[1]:
                    good = 0
                    break

        dig = randint(0, 100)
        if dig < 35:
            return MovingPlatform(x,y)
        elif dig >= 35 and dig < 50:
            return CrashingPlatform(x,y)
        else:
            return Platform(x,y)

    def draw(self):
        if self.doodle.alive == 1:
            if int(self.doodle.score / 10) >= 150:
                if self.monster == None:
                    case = randint(-1000,5)
                    if case > 0:
                        self.monster = Monster(randint(0, screen_width), randint(-50, 50))
                        self.allsprites.add(self.monster)
                        self.monster.move()
                else:
                    self.monster.move()
                    if self.doodle.rect.colliderect(self.monster.rect):
                        self.doodle.alive = 0
                    if self.monster.y >= screen_height:
                        self.allsprites.remove(self.monster)
                        self.monster = None

            self.allsprites.clear(self.window, self.background)

            for star in self.stars:
                star.update()

            stars_to_remove = []
            for star in self.stars:
                if self.doodle.rect.colliderect(star.rect):
                    stars_to_remove.append(star)
                    self.star_count += 1
                    self.star_counter_sprite.setText(str(self.star_count))
                    if self.star_sound:
                        self.star_sound.play()
            
            for star in stars_to_remove:
                self.allsprites.remove(star)
                self.stars.remove(star)

            self.doodle.inc_y_speed(-gravitation)
            if mouse_enabled:
                self.doodle.set_x(pygame.mouse.get_pos()[0])
            else:
                if transparent_walls:
                    if self.doodle.x < 0:
                        self.doodle.set_x(screen_width)
                    elif self.doodle.x > screen_width:
                        self.doodle.set_x(0)
            self.doodle.move_y(-self.doodle.ySpeed)
            
            for spr in self.allsprites:
                if isinstance(spr, Spring) and self.doodle.get_legs_rect().colliderect(spr.get_top_surface()) and self.doodle.ySpeed <= 0:
                    spr.compress()
                    self.doodle.ySpeed = spring_speed
                    self.jump_sound.play()

                if isinstance(spr, Platform) and self.doodle.get_legs_rect().colliderect(spr.get_surface_rect()) and self.doodle.ySpeed <= 0:
                    if isinstance(spr,CrashingPlatform):
                        spr.crash()
                        self.broke_sound.play()
                        break
                    self.doodle.ySpeed = jump_speed
                    self.jump_sound.play()

                if isinstance(spr, Platform):
                    if spr.y >= screen_height:
                        self.allsprites.remove(spr)
                        platform = self.randomPlatform()
                        self.allsprites.add(platform)
                        if isinstance(platform, Platform):
                            if platform.spring:
                                self.allsprites.add(platform.spring)
                            if platform.star:
                                self.allsprites.add(platform.star)
                                self.stars.add(platform.star)

                if isinstance(spr,MovingPlatform) or (isinstance(spr,CrashingPlatform) and spr.crashed == 1):
                    spr.move()

            if self.doodle.y < horizont:
                self.doodle.inc_score(abs(self.doodle.ySpeed))
                for spr in self.allsprites:
                    if not isinstance(spr, TextSprite):
                        spr.move_y(self.doodle.ySpeed)

            self.score_sprite.setText(f"{self.doodle.name}, {int(self.doodle.score/10)}")
            self.allsprites.draw(self.window)
        else:
            self.parent.location = GameLocation(self.parent, self.doodle.name, self.character_img)

    def event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.doodle.set_x(self.doodle.x - 10)
            elif event.key == K_RIGHT:
                self.doodle.set_x(self.doodle.x + 10)

class ExitLocation(Location):
    def __init__(self, parent, name, score):
        Location.__init__(self, parent)
        self.background = pygame.image.load('img/background.png')
        print("Exiting")