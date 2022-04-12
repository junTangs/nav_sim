from re import S
from pygame.sprite import Sprite
import math
from utils.math_utils import rotate
import pygame
from entity.manager import EntityManager


class Obstacle(Sprite):
    def __init__(self,config) -> None:
        super().__init__()
        
        self.config = config
        
        self.x = 0
        self.y = 0
        self.r = 0
        
        self.image = None
        self.rect = None
        self.id = None

    
    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        self.image = pygame.image.load(self.config['image'])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        EntityManager.register(self)
    
    
    def update(self):
        pass
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)