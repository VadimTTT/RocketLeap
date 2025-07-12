# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

from locations import StartLocation, GameLocation
from config import screen_width, screen_height, fps


class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Doodle Jump")
        self.location = StartLocation(self)

    def event(self, event):
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                if isinstance(self.location, GameLocation):
                    self.location = StartLocation(self)
                elif isinstance(self.location, StartLocation):
                    sys.exit()


def main():
    game = Game()
    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)
        game.location.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            game.location.event(event)
            game.event(event)


if __name__ == "__main__":
    main()
