import pygame
from pygame.locals import *

class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load("img/player1.png").convert_alpha(),
                            pygame.image.load("img/player2.png").convert_alpha()]

        self.current_image = 0
        self.speed = 20

        self.image = pygame.image.load("img/player1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (68, 78))
        self.rect = self.image.get_rect()
        self.rect[0] = 600
        self.rect[1] = 510
        self.points = 0

    def update(self):
        self.animation()

    def animation(self):
        self.current_image = (self.current_image +1 ) %2
        self.image = self.images[self.current_image]
        self.image = pygame.transform.scale(self.image, (68, 78))


class Shot (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/shot.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 30


    def update(self):
        self.rect[1] -= self.speed
