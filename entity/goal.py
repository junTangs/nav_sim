
from re import S
from pygame.sprite import Sprite
from nav_sim.entity.manager import EntityManager
import pygame

class Goal(Sprite):
    def __init__(self,config,dt,scare_trans,coord_trans) -> None:
        super().__init__()
        self.config = config
        self.id = None
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        
        
        self.dt = dt 
        self.image = None
        self.display_image = None
        self.rect = None
        self.coord_trans = coord_trans
        self.scare_trans = scare_trans
        self.setup()
        
    
    def setup(self):
         # appearance
        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.smoothscale(self.image,self.scare_trans(self.r*2,self.r*2))

        self.display_image = self.image.copy()
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)
        EntityManager.register(self)


    def draw(self,screen):
        # appearance
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x, self.y)
        screen.blit(self.display_image,self.rect)

    
    def update(self):
        pass 