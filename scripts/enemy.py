import pygame, random, time
from pygame.locals import *


class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.animation = [pygame.image.load("img/meteor1.png").convert_alpha(),
                                pygame.image.load("img/meteor2.png").convert_alpha(),
                                pygame.image.load("img/meteor3.png").convert_alpha()]


        self.image = pygame.image.load("img/meteor1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (68, 78))
        self.rect  = self.image.get_rect()
        self.rect[0] = random.randint(10,1100)
        self.rect[1] = random.randint(10,30)
        self.speed = 1
        self.current_image = 0
        self.current_explosion = 0

    def update(self):
        self.current_image = (self.current_image +1 ) %3
        self.image = self.animation[self.current_image]
        self.image = pygame.transform.scale(self.image, (68, 78))
        self.rect[1] += self.speed
