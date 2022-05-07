
from pygame.sprite import Sprite
import math
from nav_sim.utils.math_utils import rotate
import pygame
from nav_sim.entity.manager import EntityManager


class Obstacle(Sprite):
    def __init__(self,config,dt,scare_trans,coord_trans) -> None:
        super().__init__()
        
        self.config = config
        
        self.x = 0
        self.y = 0
        self.r = 0

        self.dt = dt
        self.coord_trans = coord_trans
        self.scare_trans = scare_trans
        
        self.image = None
        self.display_image = None

        self.rect = None
        self.id = None
        self.setup()

    
    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']

        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.smoothscale(self.image,self.scare_trans(self.r*2,self.r*2))
        self.display_image = self.image.copy()

        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)
        EntityManager.register(self)
    
    
    def update(self):
        pass
    
    def draw(self,screen):
        # appearance
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x, self.y)
        screen.blit(self.display_image,self.rect)

    def set(self,**kwargs):
        self.__dict__.update(kwargs)
        self.setup()
