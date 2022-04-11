from re import S
from pygame.sprite import Sprite
import math
from nav_sim.utils.math_utils import rotate



class StaticObstacle(Sprite):
    def __init__(self,config) -> None:
        super().__init__()
        
        self.config = config
        
        self.x = 0
        self.y = 0
        self.r = 0
        
        self.image = None
        self.rect = None


        
    
    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        self.image = pygame.image.load(self.config['image'])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
    
    
    def update(self):
        pass
    