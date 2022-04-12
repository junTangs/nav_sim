
from pygame.sprite import Sprite
from entity.manager import EntityManager
import pygame

class Goal(Sprite):
    def __init__(self,config,dt,scare) -> None:
        super().__init__()
        self.config = config
        self.id = None
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        
        
        self.dt = dt 
        self.image = None
        self.rect = None
        self.l_scare = scare[0] # px/m : x axis
        self.w_scare = scare[1] # px/m : y axis
        
    
    def setup(self):
         # appearance
        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.scale(self.image,(self.r*self.l_scare,self.r*self.w_scare))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x*self.l_scare,self.y*self.w_scare)
        EntityManager.register(self)
    
    
    def update(self):
        pass 